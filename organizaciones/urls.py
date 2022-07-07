from posixpath import basename
from django.urls import path
from rest_framework.routers import SimpleRouter
from organizaciones.views import Organizaciones, Diseñadores, Fabricantes, LicenciasFabricacion, Mantenedores, Keepers, Operadores, Aprovadores,Certificadores

router = SimpleRouter()
router.register('diseñadores', Diseñadores, basename = 'diseñadores')
router.register('fabricantes', Fabricantes, basename = 'fabricantes')
router.register('licencias_fabricacion', LicenciasFabricacion, basename = 'licencias_fabricacion')
router.register('mantenedores', Mantenedores, basename = 'mantenedores')
router.register('keepers', Keepers, basename = 'keepers')
router.register('operadores', Operadores, basename = 'operadores')
router.register('aprovadores', Aprovadores, basename = 'aprovadores')
router.register('certificadores', Certificadores, basename = 'certificadores')


urlpatterns = router.urls