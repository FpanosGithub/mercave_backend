from django.urls import path
from mapas.views import MapaEjes, MapaEje

urlpatterns = [
    path('mapa_ejes', MapaEjes, name = 'mapa_ejes'),
    path('mapa_ejes/<int:pk>/', MapaEje, name = 'mapa_eje'),
]