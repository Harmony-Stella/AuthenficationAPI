from rest_framework import routers
from .viewsets import UtilisateurViewSet

router = routers.DefaultRouter()
router.register('utilisateurs', UtilisateurViewSet)

urlpatterns = router.urls
