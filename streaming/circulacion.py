from pymongo import MongoClient
from material.models import Vagon, Bogie, Eje
from red_ferroviaria.models import PuntoRed
from eventos.models import EventoEje, EventoVagon
from streaming.serializers import ObjetoPy
from datetime import datetime

ACC_TIPICA_EJE_X = 2.1
ACC_TIPICA_EJE_Y = 3.4
ACC_TIPICA_EJE_Z = 5.2


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIONES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def limpiar_ejes_sueltos(vagon, lista_ejes):
    '''Función que busca si hay ejes que se han quedado colgados y los quita del vagón'''
    # Quitamos los ejes que no están
    posibles_ejes = Eje.objects.filter(vagon = vagon)
    for eje in posibles_ejes:
        if eje.codigo not in lista_ejes:
            eje.vagon = None
            eje.save()
     
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
    aax.extend(abx)
    aay.extend(aby)
    aaz.extend(abz)

    acc = -1
    # ax
    for valor in aax:
        if valor > (ACC_TIPICA_EJE_X * 1.1):
            return 1
        if valor < (ACC_TIPICA_EJE_X * 1.1) and valor > (ACC_TIPICA_EJE_X * 0.9):
            acc = 0
    # ay
    for valor in aay:
        if valor > (ACC_TIPICA_EJE_Y * 1.1):
            return 1
        if valor < (ACC_TIPICA_EJE_Y * 1.1) and valor > (ACC_TIPICA_EJE_Y * 0.9):
            acc = 0
    
    # az
    for valor in aaz:
        if valor > (ACC_TIPICA_EJE_Z * 1.1):
            return 1
        if valor < (ACC_TIPICA_EJE_Z * 1.1) and valor > (ACC_TIPICA_EJE_Z * 0.9):
            acc = 0

    return acc

def tipo_evento(parado_ini, en_movimiento, en_nudo_ini, en_nudo_fin, diferencia):
    ''' Devuelve que tipo de evento se ha producido '''
    evento = ''
    # Si está arrancando -> EVENTO ARRANQUE
    if parado_ini == True and en_movimiento == True:   
        evento = 'START'
    # Si está parando -> EVENTO PARADA
    elif parado_ini == False and en_movimiento == False:
        evento = 'STOP'
    # Si está en circulación -> Miramos si hay EVENTO NUDO o EVENTO INTERMEDIO
    elif parado_ini == False and en_movimiento == True:                                            
        # Si entramos en NUDO ferroviario -> EVENTO NUDO
        if en_nudo_fin and en_nudo_ini == False: # entramos en NUDO ferroviario
            evento = 'NUDO'
        #  Si ha pasado un tiempo sin eventos -> EVENTO INTERMEDIO (de control)
        elif diferencia.total_seconds() > 1800:       # 30 minutos
            evento = 'CIRC'
    return evento

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class ObjetoPy(object):
    '''Convierte la estructuar en objetos con los nombres de las keys pero son todo tipo str'''
    def __init__(self, data):
        data = dict(data)
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if isinstance(value, list):
            return [self.compute_attr_value(x) for x in value]
        elif isinstance(value, dict):
            return ObjetoPy(value)
        else:
            return value

class ValoresEje():
    ''' Guarda valores del mensaje de circulación correspondientes a un eje '''
    def __init__(self, msg_eje):
        self.codigo = msg_eje.eje
        self._eje = Eje.objects.get(codigo = msg_eje.eje)
        # 1.2 Guardamos temperaturas ruedas a y b
        try:
            self.tempa = float(msg_eje.tempa)
            self.tempb = float(msg_eje.tempb)  
        except:
            self.tempa = self._eje.tempa
            self.tempb = self._eje.tempb

        self.alarma_temp = self._eje.alarma_temp
        self.alarma_aceleraciones = self._eje.alarma_aceleraciones

        # 1.3 Aceleraciones
        # 1.3.1 Aceleracion rueda A, eje X
        self.aax = []
        for i in range(10):
            try:
                self.aax.append(float(msg_eje.aax[i]))
            except:
                self.aax.append(ACC_TIPICA_EJE_X)           # Si no es un float o está fuera de rango -> le damos valor típico
        # 1.3.2 Aceleracion rueda B, eje X
        self.abx = []
        for i in range(10):
            try:
                self.abx.append(float(msg_eje.abx[i]))
            except:
                self.abx.append(ACC_TIPICA_EJE_X)           # Si no es un float o está fuera de rango -> le damos valor típico
        # 1.3.3 Aceleracion rueda A, eje Y
        self.aay = []
        for i in range(10):
            try:
                self.aay.append(float(msg_eje.aay[i]))
            except:
                self.aay.append(ACC_TIPICA_EJE_Y)           # Si no es un float o está fuera de rango -> le damos valor típico
        # 1.3.4 Aceleracion rueda B, eje Y
        self.aby = []
        for i in range(10):
            try:
                self.aby.append(float(msg_eje.aby[i]))
            except:
                self.aby.append(ACC_TIPICA_EJE_Y)           # Si no es un float o está fuera de rango -> le damos valor típico
        # 1.3.5 Aceleracion rueda A, eje Z
        self.aaz = []
        for i in range(10):
            try:
                self.aaz.append(float(msg_eje.aaz[i]))
            except:
                self.aaz.append(ACC_TIPICA_EJE_Z)           # Si no es un float o está fuera de rango -> le damos valor típico
        # 1.3.5 Aceleracion rueda A, eje Z
        self.abz = []
        for i in range(10):
            try:
                self.abz.append(float(msg_eje.abz[i]))
            except:
                self.abz.append(ACC_TIPICA_EJE_Z)           # Si no es un float o está fuera de rango -> le damos valor típico

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS DEL EJE TRAS LA CIRCULACIÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def guardar(self, vagon):
        
        self._eje.alarma_temp = self.alarma_temp
        self._eje.alarma_aceleraciones = self.alarma_aceleraciones 
        self._eje.vagon = vagon
        self._eje.tempa = self.tempa                 
        self._eje.tempb = self.tempb
        self._eje.lng = vagon.lng
        self._eje.lat = vagon.lat
        self._eje.vel = vagon.vel
        if vagon.parado:
            self._eje.estado = 'PARADO'
        else:
            self._eje.estado = 'CIRCULANDO'
        
        self._eje.save()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASE PRINCIPAL 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Circulacion():
    ''' Recoge los datos de request, los convierte a objetos python y tiene métodos para 
        disparar los eventos, alarmas y guardar en Postgres y Mongo.
    '''
    def __init__(self, data):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        obj = ObjetoPy(data)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.valida = True
        self.dt = datetime.strptime(obj.dt,'%Y-%m-%d %H:%M:%S')
        self.tipo_msg = obj.tipo_msg
        self.lng_fin = float(obj.lng)
        self.lat_fin = float(obj.lat)
        self.vel = float(obj.vel)
        self.en_movimiento = True
        self.transmitiendo = True
        self.punto_red = None
        self.nueva_alarma = False
        self.en_nudo_fin = False
        if self.tipo_msg == 'SLEEP':
            self.transmitiendo = False
        # Cargamos el código del vagón y sacamos los datos del vagón
        self.vagon = Vagon.objects.get(codigo = obj.vagon)
        # Cargamos datos del vagón iniciales
        self.lng_ini = self.vagon.lng
        self.lat_ini = self.vagon.lat
        self.parado_ini = self.vagon.parado
        self.en_nudo_ini = self.vagon.en_nudo
        self.ultimo_evento_dt = self.vagon.ultimo_evento_dt
        self.alarma = self.vagon.alarma
        if (self.lng_ini == self.lng_fin) and (self.lat_ini == self.lat_fin):
            self.en_movimiento = False
            self.vel = 0.0

        # Sacamos y verificamos la lista de ejes y valores asociados a los ejes del mensaje                
        self.ejes = []
        self.lista_ejes = []
        for msg_eje in obj.msgs_ejes:
            self.lista_ejes.append(msg_eje.eje)
            self.ejes.append(ValoresEje(msg_eje))

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS ALARMAS DE TEMPERATURA Y/O DE ACELERACIONES
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def alarma_temperatura(self, eje):
        ''' Si hay alarma NUEVA de temperatura creamos evento y devolvemos True'''
        if (eje.alarma_temp == False):
            if (umbral_temperaturas(eje.tempa, eje.tempb) > 0):
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
        diferencia = self.dt - self.ultimo_evento_dt.replace(tzinfo=None)
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
        # Guardamos mensajes de vagón y ejes en mongo_db
        #guardar_mongo()
        # Vagón
        self.vagon.lng = self.lng_fin
        self.vagon.lat = self.lat_fin
        self.vagon.vel = self.vel
        self.vagon.parado = not self.en_movimiento
        self.vagon.transmitiendo = self.transmitiendo
        self.vagon.en_nudo = self.en_nudo_fin
        self.vagon.alarma = self.alarma
        self.vagon.ultimo_evento_dt = self.ultimo_evento_dt
        self.vagon.save()
        # Ejes 
        for eje in self.ejes:  
            eje.guardar(self.vagon)         
        
        limpiar_ejes_sueltos(self.vagon, self.lista_ejes) # Siguiente versión metemos los bogies también                                          
        