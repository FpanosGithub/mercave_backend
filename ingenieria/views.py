from django.shortcuts import render
from rest_framework import generics, viewsets
#from ingenieria.permisos import IsJefeOrReadOnly
from ingenieria.models import VersionEje, VersionCambiador
from ingenieria.serializers import VersionEjeSerializer, VersionCambiadorSerializer

# Create your views here.

class VersionesEjes(viewsets.ModelViewSet):
    queryset = VersionEje.objects.all()
    serializer_class = VersionEjeSerializer

class VersionesCambiadores(viewsets.ModelViewSet):
    queryset = VersionCambiador.objects.all()
    serializer_class = VersionCambiadorSerializer
