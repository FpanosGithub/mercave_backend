from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from streaming.circulacion import Circulacion
from streaming.cambio import CambioEje


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def MensajeCirculacion(request):
    #try:
    circulacion = Circulacion(request.data)
    circulacion.eventos()
    circulacion.guardar()
    return Response(request.data)
    #return Response(request.data, status = status.HTTP_201_CREATED)

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def MensajeCambio(request):
    #try:
    cambio_eje = CambioEje(data = request.data)
    cambio_eje.alarma_cambio()
    cambio_eje.guardar()
    return Response(request.data)
    