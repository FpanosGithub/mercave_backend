from pymongo import MongoClient
from material.models import Vagon, Bogie, Eje
from red_ferroviaria.models import PuntoRed
from eventos.models import EventoEje
from streaming.serializers import ObjetoPy
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
# FUNCIONES AUXILIARES A FUNCIÓN COMPROBAR EVENTOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def punto_red (lng, lat):
    puntored = PuntoRed.objects.filter(lng = lng).filter(lat = lat)[0]
    if puntored.exists():
        return puntored
    return None

def actualizar_vagon(vagon, ejes, lista_ejes, data):
    # Quitamos los ejes que no están y creamos evento para el eje que se mueve
    posibles_ejes = Eje.objects.filter(vagon = vagon)
    for eje in posibles_ejes:
        if eje.codigo not in lista_ejes:
            eje.vagon = None
            eje.save()
    # Ponemos los nuevos ejes
    ejes_actuales = Eje.objects.filter(codigo__in = lista_ejes)  
    for eje in ejes_actuales:
        if eje.vagon != vagon:
            eje.vagon = vagon
            eje.save()

def umbral_temperaturas(tempa, tempb):
    if tempa >55 or tempa < -20 or tempb >55 or tempb < -20:
        return 1
    elif tempa < 50 and tempa > -15 and tempb < 50 and tempb > -15:
        return -1
    else:
        return 0
             
def umbral_aceleraciones(msg_eje):
    acc = -1
    # aax
    for valor in msg_eje.aax:
        if valor > 2.2:
            return 1
        if valor < 2.2 and valor > 2.0:
            acc = 0
    return acc


def comprobar_alarmas (circulacion, vagon, ejes):
    ''' Dado un mensaje de circulación (circulación) para un vagón y un conjunto de ejes 
        chequeamos eje por eje si los datos del mensajes de circulación generan una alarma
        de temperatura o de aceleraciones para ese eje y en consecuencia para el vagón.
    '''
    nueva_alarma = False
    tipo = ''
    # Recorremos eje a eje.
    for eje in ejes:
        # Buscamos la información del mensaje de circulación correspondiente a ese eje
        for msg_eje in circulacion.msgs_ejes:
            if msg_eje.eje == eje.codigo:             # una vez encontrada
                # TEMPERATURAS
                # Valoramos la temperatura de cada rueda -> si hay alarma activamos
                if eje.alarma_temp == False and umbral_temperaturas(msg_eje.tempa, msg_eje.tempb) > 0:
                    eje.alarma_temp = True
                    vagon.alarma_temp = True
                    nueva_alarma = True
                    tipo = 'ALARM_TEMP'
                elif eje.alarma_temp == True and umbral_temperaturas(msg_eje.tempa, msg_eje.tempb) < 0:   
                    eje.alarma_temp = False
                    vagon.alarma_temp = False
                # ACELERACIONES
                # Valoramos las aceleraciones de cada rueda -> si hay alarma activamos
                if eje.alarma_aceleraciones == False and umbral_aceleraciones(msg_eje) > 0:
                        eje.alarma_aceleraciones = True
                        vagon.alarma_aceleraciones = True
                        nueva_alarma = True
                        tipo = 'ALARM_ACEL'
                elif eje.alarma_aceleraciones == True and umbral_aceleraciones(msg_eje) < 0:
                        eje.alarma_aceleraciones = False
                        vagon.alarma_aceleraciones = False

    return nueva_alarma, tipo
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIÓN PRINCIPAL: comprobar_eventos
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def procesar_mensaje(mensaje):
    ''' Nos han pasado un mensaje de movimiento de vagón e inspeccionamos si hay que 
        mover los elementos y/o crear un evento
    '''
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 0. OBTENEMOS LA INFORMACIÓN QUE VIENE EN EL MENSAJE DE CIRCULACIÓN ENVIADO DESDE UN VAGÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CONVERTIMOS EL MENSAJE (dict) A UN OBJETO PYTHON ESTRUCTURADO
    circulacion = ObjetoPy(mensaje)
    # EXTAREMOS DATOS
    dt = datetime.strptime(circulacion.ts,'%Y-%m-%d %H:%M:%S')      # Fecha / hora de la circualción reportada
    lista_ejes = []                                                 # Que ejes van en el vagón de la circulación
    for msg_eje in circulacion.msgs_ejes:
        lista_ejes.append(msg_eje.eje)
    nueva_lng = float(circulacion.lng)                              # Nueva longitud indicada en el mensaje de circulación
    nueva_lat = float(circulacion.lat)                              # Nueva lat
    nueva_vel = float(circulacion.vel)                              # Nueva vel

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 1. TRAEMOS LOS OBJETOS DEL SISTEMA MERCAVE QUE VAMOS A ACTUALIZAR
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # OBJETOS SISTEMA MERCAVE A ACTUALIZAR
    vagon = Vagon.objects.filter(codigo = circulacion.vagon)[0]     # Extraemos el objeto vagón de la circulación
    ejes = Eje.objects.filter(codigo__in = lista_ejes)              # Extraemos los ejes de la lista de ejes
    # GUARDAMOS LOS VALORES QUE NECESITAREMOS MÁS ADELANTE
    lng_ini = vagon.lng                                             # lng antes del mensaje
    lat_ini = vagon.lat                                             # lat antes del mensaje
    vagon_parado_ini = vagon.parado                                 # Situación del vagón antes del mensaje (True/False)
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2. ACTUALIZAMOS VALORES EN OBJETOS DEL SISTEMA MERCAVE
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # PASAMOS LOS NUEVOS VALORES 
    vagon.lng = nueva_lng                                           # lng del mensaje
    vagon.lat = nueva_lat                                           # lat del mensaje
    vagon.vel = nueva_vel                                           # velocidad del mensaje
    for eje in ejes:                                            # Para cada eje
            eje.lng = nueva_lng                                     # lng del mensaje
            eje.lat = nueva_lat                                     # lat del mensaje
            eje.vel= nueva_vel                                      # velocidad del mensaje
    # SI EL VAGÓN ESTÁ CIRCULANDO
    if (lng_ini != nueva_lng or lat_ini != nueva_lat) and nueva_vel > 1: # 1 m/s = 3,6 Km/h 
        vagon.parado = False
    # SI EL VAGÓN ESTÁ PARADO
    else:
        vagon.parado = True
        vagon.vel = 0.0
    # SI EL MENSAJE ES DE DESPERTAR O DE CIRCULAR PERO LA TRANSMISIÓN ESTÁ PARADA, PONEMOS EL VAGÓN EN MODO DESPIERTO
    if (circulacion.tipo_msg == 'WAKE' or circulacion.tipo_msg == 'CIRC') and vagon.transmitiendo == False:
        vagon.vagon.transmitiendo == True

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 3. ACTUALIZAMOS LA COMPOSICIÓN DEL VAGÓN SEGÚN MENSAJE
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    actualizar_vagon(vagon, lista_ejes) # Siguiente versión metemos los bogies también

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 4. EVENTOS DE CIRCULACIÓN - Arranque / Parada / evento intermedio
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    evento = ''                     # Le vamos a dar valores - Inicializamos
    situacion_vagon = None          # Le vamos a dar valores - Inicializamos

    # SI VAGÓN HA ARRANCADO, PARADO, ENTRA EN NUDO, HAN PASADO 30 min
    # -> DISPARAMOS EVENTOS

    # SI ESTÁ ARRANCANDO -> EVENTO ARRANQUE
    if vagon_parado_ini == True and vagon.parado == False:   
        evento = 'START'
        situacion_vagon = punto_red(nueva_lng, nueva_lat)
    # SI ESTÁ PARANDO -> EVENTO PARADA
    elif vagon_parado_ini == False and vagon.parado == True:
        evento = 'STOP'
        situacion_vagon = punto_red(nueva_lng, nueva_lat)    
    # SI ESTÁ EN CIRCULACIÓN -> MIRAMOS SI HAY EVENTO NUDO O EVENTO INTERMEDIO
    elif vagon_parado_ini == False and vagon.parado == False:                                            
        # SI ENTRAMOS EN NUDO FERROVIARIO -> EVENTO NUDO
        situacion_vagon = punto_red(nueva_lng, nueva_lat)
        if situacion_vagon.nudo == True and vagon.en_nudo == False: # ENTRAMOS EN NUDO FERROVIARIO
            vagon.en_nudo == True
            evento = 'NUDO'
        elif situacion_vagon.nudo == False:       # SINO NO ESTAMOS EN NUDO NO HAY EVENTO PERO ACTUALIZAMOS ESTADO EN VAGÓN
            vagon.en_nudo == False
        #  SI HA PASADO UN TIEMPO SIN EVENTOS -> EVENTO INTERMEDIO (de control)
        diferencia = dt - vagon.ultimo_evento_dt
        if diferencia.total_seconds() > 1800:       # 30 minutos - AJUSTAR AL TIEMPO MAX. QUE QUERAMOS ENTRE EVENTOS!!!!
            evento = 'CIRC'

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2. EVENTOS POR NUEVA ALARMA - temperatura / circulacion
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 2.2. SI DETECTAMOS NUEVA ALARMA DE TEMPERATURA O DE ACELERACIONES
    #      -> DISPARAMOS EVENTOS
    nueva_alarma, tipo = comprobar_alarmas (circulacion, vagon, ejes)
    if nueva_alarma:
        evento = tipo
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # CREAMOS EVENTOS -> 1 para el vagón uno para cada eje
    if evento == 'START' or evento == 'STOP' or evento == 'NUDO' or evento == 'CIRC' or evento == 'ALARM_TEMP' or evento == 'ALARM_ACEL':
        vagon.ultimo_evento_dt = dt
        # evento_vagon()
        for eje in ejes:
            EventoEje(
                    timestamp = dt,
                    eje = eje,
                    en_vagon = vagon, 
                    lng = nueva_lng, 
                    lat = nueva_lat,
                    punto_red = situacion_vagon,
                    evento = evento,
                    ).save()

    #subir_mongo(request.data)
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # FIN !!!!! GUARDAMOS DATOS EN OBJETOS MERCAVE
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vagon.save()
    for eje in ejes:
        eje.save()