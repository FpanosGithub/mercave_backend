from pymongo import MongoClient
from material.models import Vagon, Bogie, Eje
from red_ferroviaria.models import PuntoRed
from eventos.models import EventoEje
from datetime import datetime

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIONES DE MONGO DB
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def subir_mongo(msg):
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_db = client.mercave_mongo
    mercave_db.mensajes_circulacion.insert_one(msg)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIONES AUXILIARES DE comprobar_eventos
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def comprobar_punto_red (lng, lat):
    punto_red = PuntoRed.objects.filter(lng = lng).filter(lat = lat)[0]
    if punto_red.exists():
        return punto_red
    return None

def comprobar_ultimo_evento (vagon, ejes, nueva_lng, nueva_lat, dt):
    # Si el último evento de circulacion fue hace más de 30 min, creamos un nuevo evento de circulación
    diferencia = dt - vagon.ultimo_evento_dt
    if diferencia.total_seconds() > 1800: # 30 minutos - AJUSTAR!!!!
        vagon.ultimo_evento_circ = True
        vagon.ultimo_evento_dt = dt
        # evento_vagon()
        for eje in ejes:
            EventoEje(
                timestamp = dt,
                eje = eje,
                en_vagon = vagon, 
                lng = nueva_lng, 
                lat = nueva_lat,
                punto_red = comprobar_punto_red (nueva_lng, nueva_lat),
                evento = 'CIRC',
                ).save()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIÓN PRINCIPAL: comprobar_eventos
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def comprobar_eventos(data):
    ''' Nos han pasado un mensaje de movimiento de vagón e inspeccionamos si hay que 
        mover los elementos y/o crear un evento'''
    # Cargamos todos los elementos del mensaje y del sistema Mercave para trabajar con ellos:
    # Datos del mensaje
    dt = datetime.strptime(data.ts,'%Y-%m-%d %H:%M:%S')
    lista_ejes = []
    for msg_eje in data.msgs_ejes:
        lista_ejes.append(msg_eje.eje)
    vagon = Vagon.objects.filter(codigo = data.vagon)[0]
    ejes = Eje.objects.filter(codigo__in = lista_ejes)  
    # Guardamos los valores de estado del vagón posición iniciales y finales
    lng_ini = vagon.lng                 # lng antes del mensaje
    lat_ini = vagon.lat                 # lat antes del mensaje
    lng_fin = float(data.lng)           # lng del mensaje
    lat_fin = float(data.lat)           # lat del mensaje
    vel = vagon.vel
    transmitiendo = vagon.transmitiendo
    vagon_parado = vagon.parado     # Situación del vagón antes del mensaje
    
    

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 1. Evento de formación
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    flag_evento_form = False



    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2. Evento de Posición
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    flag_evento_pos = False


    # miramos si ha cambiado la posición
    cambio_posicion = False
    if lng_ini != lng_fin or lat_ini != lat_fin:
        cambio_posicion = True

    # Guardamos nueva posicion del vagon y sus elementos
    if cambio_posicion:
        vagon.lng = lng_fin
        vagon.lat = lat_fin
        for eje in ejes:
            eje.lng = lng_fin
            eje.lat = lat_fin

    # 2. Comprobamos formación del vagón
    # 2.1 Si otros ejes distintos a los del mensaje estan tambien en el vagón los quitamos de este
    posibles_ejes = Eje.objects.filter(vagon = vagon)
    for eje in posibles_ejes:
        if eje.codigo not in lista_ejes:
            eje.vagon = None
            eje.save()
    # 2.1 Si algun eje del mensaje no estaba en el vagon lo incluimos y creamos evento de cambio
    for eje in ejes:
        if eje.vagon != vagon:
            EventoEje(
            timestamp = dt,
            eje = eje,
            en_vagon = vagon, 
            lng = lng_fin, 
            lat = lat_fin,
            punto_red = comprobar_punto_red (lng_fin, lat_fin),
            evento = 'VAGON',
            ).save()
    
    # 3. miramos si el vagón ha arrancado o parado
    if vagon_parado and cambio_posicion:    # Evento de Arranque
        vagon.parado = False
        vagon.ultimo_evento_circ = True
        vagon.ultimo_evento_dt = dt
        # evento_vagon()
        for eje in ejes:
            EventoEje(
                    timestamp = dt,
                    eje = eje,
                    en_vagon = vagon, 
                    lng = lng_fin, 
                    lat = lat_fin,
                    punto_red = comprobar_punto_red (lng_fin, lat_fin),
                    evento = 'START',
                    ).save()
    if not vagon_parado and not cambio_posicion:    # Evento de parada
        vagon.parado = True
        vagon.ultimo_evento_circ = True
        vagon.ultimo_evento_dt = dt
        # evento_vagon()
        for eje in ejes:
            EventoEje(
                    timestamp = dt,
                    eje = eje,
                    en_vagon = vagon, 
                    lng = lng_fin, 
                    lat = lat_fin,
                    punto_red = comprobar_punto_red (lng_fin, lat_fin),
                    evento = 'STOP',
                    ).save()

    # 4. Miramos si hemos pasado por un punto de red conocido
    #if not vagon_parado:
        #punto_red = comprobar_punto_red(lng_fin, lat_fin)
        #if punto_red.nudo:
          #for eje in ejes:
            #EventoEje(
                    #timestamp = dt,
                    #eje = eje,
                    #en_vagon = vagon.codigo, 
                    #lng = lng_fin, 
                    #lat = lat_fin,
                    #punto_red = comprobar_punto_red (lng_fin, lat_fin),
                    #evento = 'NUDO',
                    #).save()  
    # 5. Si han pasdo más de 15 min en movimiento -> generamos evento circulacion
    #if not vagon_parado:
    #    comprobar_ultimo_evento(vagon, ejes, nueva_lng = lng_fin, nueva_lat = lat_fin, dt = dt)

    # 6. Pasamos a IA para ver si hay alarmas

    # FIN !!!!!
    vagon.save()
    for eje in ejes:
        eje.save()