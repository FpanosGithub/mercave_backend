from posixpath import basename
from django.urls import path
from rest_framework.routers import SimpleRouter
from ingenieria.views import VersionesEjes, VersionesCambiadores

router = SimpleRouter()
router.register('versiones_ejes', VersionesEjes, basename = 'versiones_ejes')
router.register('versiones_cambiadores', VersionesCambiadores, basename = 'versiones_cambiadores')

urlpatterns = router.urls