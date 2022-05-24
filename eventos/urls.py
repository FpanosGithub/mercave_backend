from posixpath import basename
from django.urls import path

from rest_framework.routers import SimpleRouter
from eventos.views import Cambios, Mantenimientos, AlarmasCambios, AlarmasTemp, AlarmasAceleracion, EventosEje

router = SimpleRouter()
router.register('', EventosEje, basename = 'Evento_eje')
router.register('cambios', Cambios, basename = 'cambios')
router.register('mantenimientos', Mantenimientos, basename = 'mantenimientos')
router.register('alarmas_cambios', AlarmasCambios, basename = 'alarmas_cambios')
router.register('alarmas_temp', AlarmasTemp, basename = 'alarmas_temp')
router.register('alarmas_aceleracion', AlarmasAceleracion, basename = 'alarmas_aceleracion')

urlpatterns = router.urls