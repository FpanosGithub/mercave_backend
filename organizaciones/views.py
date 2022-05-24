from django.shortcuts import render
from rest_framework import generics, viewsets

#from organizaciones.permisos import IsJefeOrReadOnly

from organizaciones.models import Organizacion, Diseñador, Fabricante, LicenciaFabricacion
from organizaciones.models import Mantenedor, Keeper, Operador, Aprovador, Certificador
from organizaciones.serializers import OrganizacionSerializer, DiseñadorSerializer, FabricanteSerializer, LicenciaFabricacionSerializer
from organizaciones.serializers import MantenedorSerializer, KeeperSerializer, OperadorSerializer, AprovadorSerializer, CertificadorSerializer

# Create your views here.

class Organizaciones(viewsets.ModelViewSet):
#    permission_classes = (IsJefeOrReadOnly,)
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer

class Diseñadores(viewsets.ModelViewSet):
    queryset = Diseñador.objects.all()
    serializer_class = DiseñadorSerializer

class Fabricantes(viewsets.ModelViewSet):
    queryset = Fabricante.objects.all()
    serializer_class = FabricanteSerializer

class LicenciasFabricacion(viewsets.ModelViewSet):
    
    queryset = LicenciaFabricacion.objects.all()
    serializer_class = LicenciaFabricacionSerializer

class Mantenedores(viewsets.ModelViewSet):
    queryset = Mantenedor.objects.all()
    serializer_class = MantenedorSerializer

class Keepers(viewsets.ModelViewSet):
    queryset = Keeper.objects.all()
    serializer_class = KeeperSerializer

class Operadores(viewsets.ModelViewSet):
    queryset = Operador.objects.all()
    serializer_class = OperadorSerializer

class Aprovadores(viewsets.ModelViewSet):
    queryset = Aprovador.objects.all()
    serializer_class = AprovadorSerializer

class Certificadores(viewsets.ModelViewSet):
    queryset = Certificador.objects.all()
    serializer_class = CertificadorSerializer
