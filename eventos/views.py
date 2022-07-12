from time import strftime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from pymongo import MongoClient
from datetime import datetime, timedelta
#!!!!!!!!!!!!!#
from eventos.models import EventoEje
from material.models import Eje
from eventos.serializers import EventoEjeSerializer, DatosCirculacion
#!!!!!!!!!!!!!#

# Views de Eventos.

@api_view()
@permission_classes([AllowAny])
def EventosEje(request, pk):
    #try:
    eventos_eje = EventoEje.objects.filter(eje__id=pk)
    serializer = EventoEjeSerializer(eventos_eje, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def DatosCirculacionEje(request, pk):
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # sacamos código del eje (si guardaramos el id del eje en Mongo no seria necesario
    # y además la busqueda en Mongo sería mucho más rápida. <MIRAR FUTURO>
    eje = Eje.objects.get(id = pk)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Rango de valores que vamos a buscar en Mongo
    fecha_inicio = request.data['comienzo']
    fecha_fin = request.data['fin']
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print('#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('#Rango de valores que vamos a buscar en Mongo')
    print(fecha_inicio)
    print(fecha_fin)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Mongo
    # inicializamos MONGO_DB para guardar datos de circulacion del eje
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_mongo = client.mercave_mongo
    cursor = mercave_mongo.circulaciones_ejes.find(
        {'eje':eje.codigo, 'tipo_msg':'CIRC','dt':{"$gt": fecha_inicio, "$lt": fecha_fin}},    # Filtro
        ['vel','tempa','tempb','aax','aay','aaz','abx','aby','abz']                             # Proyección
        ).limit(30).sort([('dt',-1)])

    serializer = DatosCirculacion(cursor)

    return Response(serializer.data)