import json
from django.shortcuts import render

from .models import Utilisateur
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from .serializer import UtilisateurReponseSerializer, UtilisateurRequestSerializer
import jwt, datetime
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


#Inscription utilisateur
class UtilisateurRegisterView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurRequestSerializer
    permission_classes = (permissions.AllowAny)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

#Connexion utilisateur
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = Utilisateur.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('Aucun Utilisateur Trouvé!')
        if not  user.check_password(password):
            raise AuthenticationFailed('Mot de Passe Incorrect!')
        
        payload = {
            'id': user.id,
            'type_utilisateur': user.type_utilisateur,
            'email':user.email,
            'nom':user.nom,
            'prenom':user.prenom,
            'username':user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
#Utilisateur  connecté
class ConnectedUserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthencated!')
        except (jwt.DecodeError, jwt.InvalidTokenError) as e:
            raise AuthenticationFailed('Invalid token: {}'.format(e))
        
        user = Utilisateur.objects.filter(idUser=payload['id']).first()
        if not user:
            raise AuthenticationFailed("Utilisateur non trouvé!")
        serializer = UtilisateurReponseSerializer(user)
        return Response({'connected-user' :serializer.data})
    
#Déconnexion
class LogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {
            'message':'success'
        }
        return response
    
#Rénitialiser le mot de passse
class ResetPasswordView(APIView):
    def post(self, request,id):
        # Récupérer les données de la requête
        ancien_mot_de_passe =  json.loads(request.data.get('old'))
        nouveau_mot_de_passe =  json.loads(request.data.get('new'))

        # Vérifier si l'utilisateur est authentifié (vous pouvez ajouter une authentification à l'aide de JWT, par exemple)
        # if not request.user.is_authenticated:
        #     return Response("Vous devez être connecté pour changer le mot de passe.", status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer l'utilisateur actuellement authentifié
        utilisateur=Utilisateur.objects.get(authuser_ptr_id=id)        # Vérifier si l'ancien mot de passe fourni correspond au mot de passe actuel de l'utilisateur
        if not utilisateur.check_password(ancien_mot_de_passe):
            return Response("L'ancien mot de passe fourni est incorrect.", status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le mot de passe de l'utilisateur avec le nouveau mot de passe haché
        utilisateur.password = make_password(nouveau_mot_de_passe)
        utilisateur.save()

        return Response("Le mot de passe a été changé avec succès.", status=status.HTTP_200_OK)
    
#Suppression de compte
class DeleteAccount(APIView):
    def delete(self, request, id):
        try:
            artisan = Utilisateur.objects.get(authuser_ptr_id=id)
            artisan.delete()
            return Response("Suppresion du Compte Réussie", status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            return Response({'error': 'Artisan not found'}, status=status.HTTP_404_NOT_FOUND)
