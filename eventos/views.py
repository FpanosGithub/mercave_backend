from time import strftime
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from pymongo import MongoClient
from eventos.logicas import calcular_rango_evento
#!!!!!!!!!!!!!#
from eventos.models import EventoEje
from eventos.serializers import EventoEjeSerializer, DatosCirculacion
#!!!!!!!!!!!!!#

# Views de Eventos.

@api_view()
@permission_classes([AllowAny])
def EventosEje(request, pk):
    #try:
    eventos_eje = EventoEje.objects.filter(eje__id=pk).order_by('-dt')
    serializer = EventoEjeSerializer(eventos_eje, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def DetallesEvento(request, pk):
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # sacamos código del eje (si guardaramos el id del eje en Mongo no seria necesario
    # y además la busqueda en Mongo sería mucho más rápida. <MIRAR FUTURO>
    eje = request.data['eje']
    dt = request.data['dt']
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Rango de valores que vamos a buscar en Mongo
    dt_inicio, dt_fin = calcular_rango_evento(dt, 3600)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print('#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('#Rango de valores que vamos a buscar en Mongo')
    print(dt)
    print(dt_fin)
    print(dt_inicio)
    print(eje)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Mongo
    # inicializamos MONGO_DB para guardar datos de circulacion del eje
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_mongo = client.mercave_mongo
    cursor = mercave_mongo.circulaciones_ejes.find(
        {'eje':eje, 'dt':{"$gt": dt_inicio, "$lt": dt_fin}},            # Filtro
        ['vel','tempa','tempb','aax','aay','aaz','abx','aby','abz']     # Proyección
        ).limit(300).sort([('dt',-1)])

    serializer = DatosCirculacion(cursor)
    
    return Response(serializer.data)
