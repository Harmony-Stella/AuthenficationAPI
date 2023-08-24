from rest_framework import serializers
from .models import Utilisateur

class UtilisateurRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'username', 'password', 'code_matricule']

class UtilisateurReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id','nom', 'prenom', 'email', 'username', 'password', 'profile_photo']

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
