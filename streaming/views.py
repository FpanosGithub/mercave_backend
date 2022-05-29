from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from streaming.serializers import ValidadorMensajeCirculacion
from streaming.mensajes_hht import data3num
from streaming.circulacion import Circulacion


# Create your views here.
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def MensajeCirculacion(request):
    if request.method == 'GET':
        data = data3num
        mensaje = ValidadorMensajeCirculacion(data=data)
        if mensaje.is_valid():
            return Response(data)
            #return Response(mensaje.data)
        return Response(mensaje.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        circulacion = Circulacion(request.data)
        #mensaje = ValidadorMensajeCirculacion(data = request.data)
        if circulacion.valida:
            #subir_mongo(request.data)
            #circulacion = ObjetoPy(request.data)
            #procesar_mensaje(circulacion)
            # procesar_mensaje(mensaje)
            circulacion.eventos()
            circulacion.guardar()
            return Response(request.data, status = status.HTTP_201_CREATED)
    return Response(circulacion.error, status=status.HTTP_400_BAD_REQUEST)

