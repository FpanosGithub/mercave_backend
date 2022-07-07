from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
#!!!!!
from mapas.mapas import mapa_ejes, mapa_eje
from material.models import Eje
from eventos.models import EventoEje
#!!!!!

# Views de Mapas.

@api_view()
@permission_classes([AllowAny])
def MapaEjes(request):
    #try:
    ejes = Eje.objects.all()
    mapa = mapa_ejes(ejes)
    return Response(mapa)

@api_view()
@permission_classes([AllowAny])
def MapaEje(request, pk):
    #try:
    eje = Eje.objects.get(id = pk)
    circulaciones_eje = EventoEje.objects.filter(eje=eje)
    num_circulaciones = len(circulaciones_eje)
    num_a_mostrar = 25
    if num_circulaciones <= num_a_mostrar:
        circulaciones = circulaciones_eje
    else:
        circulaciones = circulaciones_eje[(num_circulaciones - num_a_mostrar): num_circulaciones]

    mapa = mapa_eje(eje, eventos = circulaciones)
    return Response(mapa)