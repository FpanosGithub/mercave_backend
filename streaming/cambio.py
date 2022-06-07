from pymongo import MongoClient
from material.models import Eje, Cambiador
from eventos.models import AlarmaCambio, EventoEje, EventoVagon, Cambio
from red_ferroviaria.models import PuntoRed
from datetime import datetime
import pytz

FMAX_TIPICA_DESENCERROJAMIENTO = 31
FMAX_TIPICA_CAMBIO = 26
FMIN_TIPICA_ENCERROJAMIENTO = 0.1

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIONES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def punto_red (lng, lat):
    ''' Función que busca si estamos en un punto singular de la red '''
    try:
        puntored = PuntoRed.objects.filter(lng = lng).filter(lat = lat)
    except:
        return None, False

    return None, False  
    # return puntored, puntored.nudo
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class ValoresCambio():
    def __init__(self, data):
        self.tdaM = data['tdaM']
        self.fdaM = data['fdaM']
        self.ddaM = data['ddaM']
        self.tcaM = data['tcaM']
        self.fcaM = data['fcaM']
        self.dcaM = data['dcaM']
        self.team = data['team']
        self.feam = data['feam']
        self.deam = data['deam']
        self.tdbM = data['tdbM']
        self.fdbM = data['fdbM']
        self.ddbM = data['ddbM']
        self.tcbM = data['tcbM']
        self.fcbM = data['fcbM']
        self.dcbM = data['dcbM']
        self.tebm = data['tebm']
        self.febm = data['febm']
        self.debm = data['debm']
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASE PRINCIPAL 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class CambioEje():
    ''' Recoge los datos del request, los convierte a objetos python y tiene métodos para 
        disparar los eventos, alarmas y guardar en Postgres y Mongo.
    '''
    def __init__(self, data):
        self.codigo_eje = data['eje']
        self.eje = Eje.objects.get(codigo = self.codigo_eje)
        self.alarma = data['alarma']
        self.mensaje_alarma = ''
        self.inicio = datetime.strptime(data['inicio'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Europe/Madrid'))
        self.codigo_cambiador = data['cambiador']
        self.cambiador = Cambiador.objects.get(codigo = self.codigo_cambiador)
        self.sentido = data['sentido']
        self.V = data['V']
        self.FV = data['FV']
        self.valores_cambio = ValoresCambio(data= data)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS ALARMA
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def alarma_cambio(self):
        ''' Si hay alarma creamos evento de eje y creamos alarma de cambio'''
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Mas adelante evaluaremos el cambio en el módulo de IA. Haremos
        # un request a la API correspondiente pasando los valores del cambio
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #||||||||   alarma = cambio.ml.predict(self.valores_cambio)   |||||||||
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # fuerza de descerrojamiento en ruedas A y B.
        if (self.valores_cambio.fdaM > FMAX_TIPICA_DESENCERROJAMIENTO) or (self.valores_cambio.fdbM > FMAX_TIPICA_DESENCERROJAMIENTO):
            self.alarma = True
            self.mensaje_alarma = 'Fuerza excesiva sobre el disco de empuje en el proceso de desencerrojamiento'
        # fuerza de descerrojamiento en ruedas A y B.
        if (self.valores_cambio.fcaM > (FMAX_TIPICA_CAMBIO) or (self.valores_cambio.fcaM > FMAX_TIPICA_CAMBIO)):
            self.alarma = True
            self.mensaje_alarma = 'Fuerza excesiva sobre la rueda en el proceso de cambio de ancho'
        # fuerza de descerrojamiento en ruedas A y B.
        if (self.valores_cambio.fcaM < FMIN_TIPICA_ENCERROJAMIENTO) or (self.valores_cambio.fcaM < FMIN_TIPICA_ENCERROJAMIENTO):
            self.alarma = True
            self.mensaje_alarma = 'El disco de empuje quedó enganchado en el proceso de encerrojamiento'
        self.alarma = False
       
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS DEL CAMBIO
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def guardar(self):
        # inicializamos MONGO_DB para guardar mensajes de vagón y ejes
        # cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
        # client = MongoClient(cluster)    
        # mercave_mongo = client.mercave_mongo
        # Cambio
        cambio = Cambio(
            eje = self.eje,
            alarma = self.alarma,
            inicio = self.inicio,
            cambiador = self.cambiador,
            sentido = self.sentido,
            V = self.V,
            FV = self.FV,
            tdaM = self.valores_cambio.tdaM,
            fdaM = self.valores_cambio.fdaM,
            ddaM = self.valores_cambio.ddaM,
            tcaM = self.valores_cambio.tcaM,
            fcaM = self.valores_cambio.fcaM,
            dcaM = self.valores_cambio.dcaM,
            team = self.valores_cambio.team,
            feam = self.valores_cambio.feam,
            deam = self.valores_cambio.deam,
            tdbM = self.valores_cambio.tdbM,
            fdbM = self.valores_cambio.fdbM,
            ddbM = self.valores_cambio.ddbM,
            tcbM = self.valores_cambio.tcbM,
            fcbM = self.valores_cambio.fcbM,
            dcbM = self.valores_cambio.dcbM,
            tebm = self.valores_cambio.tebm,
            febm = self.valores_cambio.febm,
            debm = self.valores_cambio.debm,
            ).save()
        # Guardamos evento eje del cambio
        EventoEje(
            dt = self.inicio,
            eje = self.eje,
            en_vagon = self.eje.vagon, 
            lng = self.cambiador.lng, 
            lat = self.cambiador.lng,
            punto_red = None,
            evento = 'CAMBIO',
            ).save()  
        # Si hay alarma guardamos Alarma Cambio y evento alarma cambio
        if self.alarma:
            AlarmaCambio(
            cambio = cambio,
            mensaje = self.mensaje_alarma,
            ).save()

                                           