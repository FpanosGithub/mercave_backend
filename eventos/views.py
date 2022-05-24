from django.shortcuts import render
from rest_framework import generics, viewsets

#from organizaciones.permisos import IsJefeOrReadOnly

from eventos.models import Cambio, Mantenimiento, AlarmaCambio, AlarmaTemp, AlarmaAceleracion, EventoEje
from eventos.serializers import CambioSerializer, MantenimientoSerializer, AlarmaCambioSerializer, AlarmaTempSerializer, AlarmaAceleracionSerializer, EventoEjeSerializer

# Create your views here.

class Cambios(viewsets.ModelViewSet):
    queryset = Cambio.objects.all()
    serializer_class = CambioSerializer

class Mantenimientos(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer

class AlarmasCambios(viewsets.ModelViewSet):
    queryset = AlarmaCambio.objects.all()
    serializer_class = AlarmaCambioSerializer

class AlarmasTemp(viewsets.ModelViewSet):
    queryset = AlarmaTemp.objects.all()
    serializer_class = AlarmaTempSerializer

class AlarmasAceleracion(viewsets.ModelViewSet):
    queryset = AlarmaAceleracion.objects.all()
    serializer_class = AlarmaAceleracionSerializer

class EventosEje(viewsets.ModelViewSet):
    queryset = EventoEje.objects.all()
    serializer_class = EventoEjeSerializer


