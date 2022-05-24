from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from streaming.logicas import subir_mongo, comprobar_eventos
from streaming.serializers import ValidadorMensajeCirculacion, ObjetoPy
from streaming.mensajes_hht import data1num


# Create your views here.
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def MensajeCirculacion(request):
    if request.method == 'GET':
        data = data1num
        mensaje = ValidadorMensajeCirculacion(data=data)
        if mensaje.is_valid():
            return Response(data)
            #return Response(msg_circ.data)
        return Response(mensaje.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        mensaje = ValidadorMensajeCirculacion(data = request.data)
        if mensaje.is_valid():
            subir_mongo(request.data)
            circulacion = ObjetoPy(request.data)
            comprobar_eventos(circulacion)
            return Response(mensaje.data, status = status.HTTP_201_CREATED)
    return Response(mensaje.errors, status=status.HTTP_400_BAD_REQUEST)

