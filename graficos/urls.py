from django.urls import path
from graficos.views import VelocidadEje

urlpatterns = [
    path('graficos/velocidad_eje/<int:pk>/', VelocidadEje, name = 'graficos_velocidad_eje'),
]