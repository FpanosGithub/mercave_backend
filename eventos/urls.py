from django.urls import path
from eventos.views import EventosEje, DetallesEvento

urlpatterns = [
    path('eventos_eje/<int:pk>/', EventosEje, name = 'eventos_eje'),
    path('detalles_evento/<int:pk>/', DetallesEvento, name = 'detalles_evento'),
]