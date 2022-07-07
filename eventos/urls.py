from django.urls import path
from eventos.views import EventosEje

urlpatterns = [
    path('eventos_eje/<int:pk>/', EventosEje, name = 'eventos_eje'),
]





#from rest_framework.routers import SimpleRouter
#from eventos.views import Cambios, Mantenimientos, AlarmasCambios, AlarmasTemp, AlarmasAceleracion, EventosEje, EventosVagon

#router = SimpleRouter()
#router.register('eventos_vagon', EventosVagon, basename = 'Evento_vagon')
#router.register('eventos_eje', EventosEje, basename = 'Evento_eje')
#router.register('cambios', Cambios, basename = 'cambios')
#router.register('mantenimientos', Mantenimientos, basename = 'mantenimientos')
#router.register('alarmas_cambios', AlarmasCambios, basename = 'alarmas_cambios')
#router.register('alarmas_temp', AlarmasTemp, basename = 'alarmas_temp')
#router.register('alarmas_aceleracion', AlarmasAceleracion, basename = 'alarmas_aceleracion')

#urlpatterns = router.urls