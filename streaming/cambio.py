from pymongo import MongoClient
from material.models import Eje, Cambiador
from eventos.models import EventoEje, EventoVagon, Cambio
from datetime import datetime
import pytz

ACC_TIPICA_EJE_X = 2.1
ACC_TIPICA_EJE_Y = 3.4
ACC_TIPICA_EJE_Z = 5.2

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

def umbral_temperaturas(tempa, tempb):
    ''' Función que determina si hemos pasado los umbrales de temperaturas admisibles + Delta -> return 1
        Si estamos por debajo los umbrales de temperaturas admisibles - Delta -> return - 1 
        o si estamos en valores de umbrales +/- Delta -> return 0
    '''
    if tempa >55 or tempa < -20 or tempb >55 or tempb < -20:
        return 1
    elif tempa < 50 and tempa > -15 and tempb < 50 and tempb > -15:
        return -1
    else:
        return 0
             
def umbral_aceleraciones(aax,abx,aay,aby,aaz,abz):
    ''' Función que determina si hemos pasado los umbrales + Delta -> return 1
        Si estamos por debajo los umbrales - Delta -> return - 1 
        o si estamos en valores de umbrales +/- Delta -> return 0
    '''
    acc = -1
    # ax
    for valor in aax:
        if valor > (ACC_TIPICA_EJE_X * 3.0):
            return 1
        elif valor > (ACC_TIPICA_EJE_X * 0.8):
            acc = 0
    # ay
    for valor in aay:
        if valor > (ACC_TIPICA_EJE_Y * 3.0):
            return 1
        elif valor > (ACC_TIPICA_EJE_Y * 0.8):
            acc = 0 
    # az
    for valor in aaz:
        if valor > (ACC_TIPICA_EJE_Z * 3.0):
            return 1
        elif valor > (ACC_TIPICA_EJE_Z * 0.8):
            acc = 0
    # bx
    for valor in abx:
        if valor > (ACC_TIPICA_EJE_X * 3.0):
            return 1
        elif valor > (ACC_TIPICA_EJE_X * 0.8):
            acc = 0
    # by
    for valor in aby:
        if valor > (ACC_TIPICA_EJE_Y * 1.1):
            return 1
        elif valor > (ACC_TIPICA_EJE_Y * 0.8):
            acc = 0
    # bz
    for valor in abz:
        if valor > (ACC_TIPICA_EJE_Z * 1.1):
            return 1
        elif valor > (ACC_TIPICA_EJE_Z * 0.8):
            acc = 0

    return acc

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
        self.inicio = datetime.strptime(data['inicio'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Europe/Madrid'))
        self.codigo_cambiador = data['cambiador']
        self.cambiador = Cambiador.objects.get(codigo = self.codigo_cambiador)
        self.sentido = data['sentido']
        self.V = data['V']
        self.FV = data['FV']
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

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS ALARMAS DE TEMPERATURA Y/O DE ACELERACIONES
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def alarma_cambio(self, eje):
        ''' Si hay alarma creamos evento y devolvemos True'''
        if (umbral_fuerzas(eje.tempa, eje.tempb) > 0):
            EventoEje(
                dt = self.dt,
                eje = eje._eje,
                en_vagon = self.vagon, 
                lng = self.lng_fin, 
                lat = self.lat_fin,
                punto_red = self.puntored,
                evento = 'ALARM_TEMP',
                ).save()  
            return 'Nueva_alarma'
        else:
            return 'Sin_alarma'
        if (eje.alarma_temp == True):
            if (umbral_temperaturas(eje.tempa, eje.tempb) < 0):
                return 'Desaparece_alarma'
            else:
                return 'Mantiene_alarma'
    
    def alarma_aceleraciones(self, eje):
        ''' Si hay alarma NUEVA de aceleraciones creamos evento y devolvemos True'''
        if (eje.alarma_aceleraciones == False):
            if (umbral_aceleraciones(eje.aax,eje.abx,eje.aay,eje.aby,eje.aaz,eje.abz) > 0):
                EventoEje(
                    dt = self.dt,
                    eje = eje._eje,
                    en_vagon = self.vagon, 
                    lng = self.lng_fin, 
                    lat = self.lat_fin,
                    punto_red = self.puntored,
                    evento = 'ALARM_ACEL',
                    ).save()  
                return 'Nueva_alarma'
            else:
                return 'Sin_alarma'
        if (eje.alarma_aceleraciones == True):
            if (umbral_aceleraciones(eje.aax,eje.abx,eje.aay,eje.aby,eje.aaz,eje.abz) < 0):
                return 'Desaparece_alarma'
            else:
                return 'Mantiene_alarma'
    
    def alarmas(self):
        ''' Chequeamos eje por eje si los datos del mensajes de circulación generan una alarma
            de temperatura o de aceleraciones para ese eje y en consecuencia para el vagón.
        '''
        sin_alarmas = True
        # Recorremos eje a eje.
        for eje in self.ejes:
            # TEMPERATURAS
            alarma = self.alarma_temperatura(eje)
            if alarma == 'Nueva_alarma':
                eje.alarma_temp = True
                sin_alarmas = False
            elif alarma == 'Mantiene_alarma':
                sin_alarmas = False
            elif alarma == 'Desaparece_alarma':
                eje.alarma_temp = False
            
            # ACELERACIONES
            # Valoramos las aceleraciones de cada rueda -> si hay alarma activamos
            alarma = self.alarma_aceleraciones(eje)
            if alarma == 'Nueva_alarma':
                eje.alarma_aceleraciones = True
                sin_alarmas = False
            elif alarma == 'Mantiene_alarma':
                sin_alarmas = False
            elif alarma == 'Desaparece_alarma':
                eje.alarma_aceleraciones = False

        if sin_alarmas:
            self.alarma = False
        else:
            self.alarma = True

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS EVENTOS
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def eventos(self):
        ''' Función que coge los datos de la circulación y chequea si hay que generar eventos o alarmas. 
            Y los genera
        '''
        
        self.puntored, self.en_nudo_fin = punto_red(self.lng_fin, self.lat_fin)
        evento = tipo_evento(self.parado_ini, self.en_movimiento, self.en_nudo_ini, self.en_nudo_fin, diferencia)

        # CREAMOS EVENTOS CIRCULACIÓN -> 1 para el vagón uno para cada eje
        if evento == 'START' or evento == 'STOP' or evento == 'NUDO' or evento == 'CIRC':
            self.vagon.ultimo_evento_dt = self.dt
            EventoVagon(
                    dt = self.dt,
                    vagon = self.vagon, 
                    lng = self.lng_fin, 
                    lat = self.lat_fin,
                    punto_red = self.puntored,
                    evento = evento,
                    ).save()
            for eje in self.ejes:
                EventoEje(
                    dt = self.dt,
                    eje = eje._eje,
                    en_vagon = self.vagon, 
                    lng = self.lng_fin, 
                    lat = self.lat_fin,
                    punto_red = self.puntored,
                    evento = evento,
                    ).save()

        # MIRAMOS NUEVA ALARMA de TEMPERATURA o de ACELERACIONES -> disparamos EVENTOS
        self.alarmas()
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS DE LA CIRCULACIÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def guardar(self):
        # inicializamos MONGO_DB para guardar mensajes de vagón y ejes
        cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(cluster)    
        mercave_mongo = client.mercave_mongo

        # Vagón
        self.vagon.lng = self.lng_fin
        self.vagon.lat = self.lat_fin
        self.vagon.vel = self.vel
        self.vagon.parado = not self.en_movimiento
        self.vagon.transmitiendo = self.transmitiendo
        self.vagon.en_nudo = self.en_nudo_fin
        self.vagon.alarma = self.alarma
        self.vagon.ultimo_evento_dt = self.ultimo_evento_dt
        # Guardamos vagón en mercave_sql
        self.vagon.save()
        # Guardamos circulación - vagón en mercave_mongo
        msg= {
            'dt': self.dt.strftime("%m/%d/%Y %H:%M:%S"), 
            'tipo_msg':self.tipo_msg,
            'vagon': self.vagon.codigo, 
            'lng':self.vagon.lng, 
            'lat':self.vagon.lat,
            'vel':self.vagon.vel,
            }
        mercave_mongo.circulaciones_vagones.insert_one(msg)

        # Ejes 
        for eje in self.ejes:  
            # Guardamos eje en mercave_sql
            eje.guardar(self.vagon)   
            # Guardamos circulación - eje en mercave_mongo
            msg= {
            'dt': self.dt.strftime("%m/%d/%Y %H:%M:%S"), 
            'tipo_msg':self.tipo_msg,
            'eje':eje.codigo,
            'en_vagon': self.vagon.codigo, 
            'lng':self.vagon.lng, 
            'lat':self.vagon.lat,
            'vel':self.vagon.vel, 
            'tempa': eje.tempa, 
            'tempb': eje.tempb, 
            'aax':eje.aax,
            'aay':eje.aay,
            'aaz':eje.aaz,
            'abx':eje.abx,
            'aby':eje.aby,
            'abz':eje.abz,
            }
            mercave_mongo.circulaciones_ejes.insert_one(msg)
               
        limpiar_ejes_sueltos(self.vagon, self.lista_ejes) # Siguiente versión metemos los bogies también                                          