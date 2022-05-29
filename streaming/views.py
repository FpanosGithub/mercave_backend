from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from streaming.circulacion import Circulacion


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def MensajeCirculacion(request):
    try:
        circulacion = Circulacion(request.data)
        circulacion.eventos()
        circulacion.guardar()
        return Response(request.data, status = status.HTTP_201_CREATED)
    except:
        return Response('No se pudo procesar mensaje de circulación', status=status.HTTP_400_BAD_REQUEST)

