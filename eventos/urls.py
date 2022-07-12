from django.urls import path
from eventos.views import EventosEje, DatosCirculacionEje

urlpatterns = [
    path('eventos_eje/<int:pk>/', EventosEje, name = 'eventos_eje'),
    path('datos_circulacion_eje/<int:pk>/', DatosCirculacionEje, name = 'datos_circulacion_eje'),
]