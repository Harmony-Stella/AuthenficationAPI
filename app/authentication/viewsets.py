from authentication.models import Utilisateur
from rest_framework import viewsets
from authentication.serializer import UtilisateurReponseSerializer, UtilisateurRequestSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method =='PUT':
            return UtilisateurRequestSerializer
        else:
            return UtilisateurReponseSerializer