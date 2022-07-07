from rest_framework import viewsets
from material.permisos import IsJefeOrReadOnly
from material.models import Composicion, Cambiador, Vagon, Bogie, Eje
from material.serializers import ComposicionSerializer, VagonSerializer, BogieSerializer, EjeSerializer, CambiadorSerializer
# Create your views here.

class Composiciones(viewsets.ModelViewSet):
    permission_classes = (IsJefeOrReadOnly,)
    queryset = Composicion.objects.all()
    serializer_class = ComposicionSerializer

class Vagones(viewsets.ModelViewSet):
    queryset = Vagon.objects.all()
    serializer_class = VagonSerializer

class Bogies(viewsets.ModelViewSet):
    queryset = Bogie.objects.all()
    serializer_class = BogieSerializer

class Ejes(viewsets.ModelViewSet):
    queryset = Eje.objects.order_by('id')
    serializer_class = EjeSerializer

class Cambiadores(viewsets.ModelViewSet):
    queryset = Cambiador.objects.all()
    serializer_class = CambiadorSerializer
