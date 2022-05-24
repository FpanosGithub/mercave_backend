from posixpath import basename
from django.urls import path
from rest_framework.routers import SimpleRouter
from material.views import Composiciones, Vagones, Bogies, Ejes, Cambiadores

router = SimpleRouter()
router.register('composiciones', Composiciones, basename = 'composiciones')
router.register('vagones', Vagones, basename = 'vagones')
router.register('bogies', Bogies, basename = 'bogies')
router.register('ejes', Ejes, basename = 'ejes')
router.register('cambiadores', Cambiadores, basename = 'cambiadores')

urlpatterns = router.urls