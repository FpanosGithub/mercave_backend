from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
#!!!!!
from eventos.models import EventoEje
from material.models import Eje
from eventos.serializers import EventoEjeSerializer
#!!!!!

# Views de Eventos.

@api_view()
@permission_classes([AllowAny])
def EventosEje(request, pk):
    #try:
    eventos_eje = EventoEje.objects.filter(eje__id=pk)
    serializer = EventoEjeSerializer(eventos_eje, many=True)

    return Response(serializer.data)
