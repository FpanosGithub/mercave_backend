from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from graficos.graficos import plotear_velocidad_eje
#!!!!!
from material.models import Eje
from eventos.models import EventoEje
#!!!!!

# Views de Gráficos.
@api_view()
@permission_classes([AllowAny])
def VelocidadEje(request, pk):
    #try:
    eje = Eje.objects.get(id = pk)
    grafico = plotear_velocidad_eje(eje.codigo)
    return Response(grafico)
