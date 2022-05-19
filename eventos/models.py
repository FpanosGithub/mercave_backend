from django.db import models
from django.urls import reverse
from material.models import Vagon, Bogie, Eje, Cambiador

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Modelos que identifican puntos singulares de la red ferroviaria
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Linea(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    nombre = models.CharField(max_length=100, null= True, blank = True)
    def __str__(self):
        return (str(self.codigo) + '-' + str(self.nombre))
    def get_absolute_url(self):
        return reverse("ficha_linea", kwargs={'pk':self.pk})

class PuntoRed(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    descripcion = models.CharField(max_length=100, null= True, blank = True)
    linea = models.ForeignKey(Linea, on_delete=models.RESTRICT, null= True, blank = True)
    pkilometrico = models.FloatField(null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    def __str__(self):
        if self.codigo: return (str(self.codigo) + ' - ' + str(self.lng) + ':' + str(self.lat))
        else: return ''
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EVENTOS DEL EJE. Llegan desde API de mercave_simulacion o mercave_circulación (IoT, IA).
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAMBIO. Cada cambio registra sus valores y dispara un evento para el eje
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Cambio(models.Model):
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    num_cambio_eje = models.IntegerField(default=0)
    alarma = models.BooleanField(default=False)
    inicio = models.DateTimeField()
    cambiador = models.ForeignKey(Cambiador, on_delete=models.RESTRICT)
    opciones_sentido =  [('UICIB', 'UIC->IB'),
                         ('IBUIC', 'IB->UIC'),
                         ('UICRUS', 'UIC->RUS'),
                         ('RUSUIC', 'RUS->UIC')]
    sentido = models.CharField(max_length=8, choices = opciones_sentido, default = 'UICIB')                 
    V = models.FloatField(default = 2.77)       # Velocidad de entrada m/s
    FV = models.FloatField(default = 250)       # Fuerza Vertical (peso en eje) KN
    # VALORES RUEDA A
    tdaM = models.FloatField(default = 5000)  # tiempo (ms) desde inicio punto de F máxima en desencerrojamiento
    fdaM = models.FloatField(default = 30)    # fuerza (KN) máxima en desencerrojamiento
    ddaM = models.FloatField(default = 10)    # desplazamiento (mm) de disco en punto de f máxima en desencerrojamiento
    tcaM = models.FloatField(default = 10000)  # tiempo (ms) desde inicio punto de F máxima en cambio
    fcaM = models.FloatField(default = 20)    # fuerza (KN) máxima en desencerrojamiento
    dcaM = models.FloatField(default = 70)  # desplazamiento (mm) de rueda en punto de F máxima en cambio
    team = models.FloatField(default = 15000)  # tiempo (ms) desde inicio punto de F minima en encerrojamiento
    feam = models.FloatField(default = 10)    # fuerza (KN) mínima en encerrojamiento
    deam = models.FloatField(default = 20)  # desplazamiento (mm) de disco en punto de F mínima en encerrojamiento
    # VALORES RUEDA B 
    tdbM = models.FloatField(default = 25000)  # tiempo (ms) desde inicio punto de F máxima en desencerrojamiento
    fdbM = models.FloatField(default = 30)    # fuerza (KN) máxima en desencerrojamiento
    ddbM = models.FloatField(default = 10)    # desplazamiento (mm) de disco en punto de f máxima en desencerrojamiento
    tcbM = models.FloatField(default = 300000)  # tiempo (ms) desde inicio punto de F máxima en cambio
    fcbM = models.FloatField(default = 20)    # fuerza (KN) máxima en desencerrojamiento
    dcbM = models.FloatField(default = 70)  # desplazamiento (mm) de rueda en punto de F máxima en cambio
    tebm = models.FloatField(default = 35000)  # tiempo (ms) desde inicio punto de F minima en encerrojamiento
    febm = models.FloatField(default = 10)    # fuerza (KN) mínima en encerrojamiento
    debm = models.FloatField(default = 20)  # desplazamiento (mm) de disco en punto de F mínima en encerrojamiento
    def __str__(self):
        return (str(self.inicio) + ' - ' + str(self.cambiador.nombre) + ' - eje: ' + str(self.eje.codigo))
    def get_absolute_url(self):
        return reverse("ficha_cambio", kwargs={'pk':self.pk})
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# MANTENIMIENTO.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Mantenimiento(models.Model):
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, null= True, blank = True)
    observaciones = models.CharField(max_length=30, null= True, blank = True)
    taller = models.CharField(max_length=30, null= True, blank = True)
    varios = models.CharField(max_length=30, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - eje: ' + str(self.eje.codigo) + ' - ' + str(self.tipo))
    def get_absolute_url(self):
        return reverse("ficha_mantenimiento", kwargs={'pk':self.pk})


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ALARMAS 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class AlarmaCambio(models.Model):
    cambio = models.ForeignKey(Cambio, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=30)
    vista = models.BooleanField(default=False)
    def __str__(self):
        return (self.mensaje)
    def get_absolute_url(self):
        return reverse("alarma_cambio", kwargs={'pk':self.pk})

class AlarmaTemp(models.Model):
    mensaje = models.CharField(max_length=30)
    vista = models.BooleanField(default=False)
    t0 = models.FloatField(default = 25)
    t1 = models.FloatField(default = 25)
    t2 = models.FloatField(default = 25)
    t3 = models.FloatField(default = 25)
    t4 = models.FloatField(default = 25)
    t5 = models.FloatField(default = 25)
    t6 = models.FloatField(default = 25)
    t7 = models.FloatField(default = 25)
    t8 = models.FloatField(default = 25)
    t9 = models.FloatField(default = 25)
    def __str__(self):
        return (self.mensaje)
    def get_absolute_url(self):
        return reverse("alarma_temperatura", kwargs={'pk':self.pk})

class AlarmaAceleracion(models.Model):
    mensaje = models.CharField(max_length=30)
    vista = models.BooleanField(default=False)
    ax0 = models.FloatField(default = 2) 
    ay0 = models.FloatField(default = 1) 
    az0 = models.FloatField(default = 0)
    ax1 = models.FloatField(default = 0)
    ay1 = models.FloatField(default = 3)
    az1 = models.FloatField(default = 4)
    ax2 = models.FloatField(default = -2)
    ay2 = models.FloatField(default = 1)
    az2= models.FloatField(default = 0)
    ax3 = models.FloatField(default = 0)
    ay3 = models.FloatField(default = -1)
    az3= models.FloatField(default = -4)
    ax4 = models.FloatField(default = 2)
    ay4 = models.FloatField(default = -3)
    az4= models.FloatField(default = 0)
    ax5 = models.FloatField(default = 0)
    ay5 = models.FloatField(default = -1)
    az5 = models.FloatField(default = 4)
    ax6 = models.FloatField(default = -2)
    ay6 = models.FloatField(default = 1)
    az6 = models.FloatField(default = 0)
    ax7 = models.FloatField(default = 0)
    ay7 = models.FloatField(default = 3)
    az7 = models.FloatField(default = -4)
    ax8 = models.FloatField(default = 2)
    ay8 = models.FloatField(default = 1)
    az8 = models.FloatField(default = 0)
    ax9 = models.FloatField(default = 0)
    ay9 = models.FloatField(default = -1)
    az9= models.FloatField(default = 4)
    def __str__(self):
        return (self.mensaje)
    def get_absolute_url(self):
        return reverse("alarma_aceleracion", kwargs={'pk_alarma':self.pk})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EVENTO DE EJE
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class EventoEje(models.Model):
    timestamp = models.DateTimeField()
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    en_bogie = models.ForeignKey(Bogie, on_delete=models.RESTRICT, null= True, blank = True)
    # en_bogie_codigo = models.CharField(max_length=16, null= True, blank = True)
    en_vagon = models.ForeignKey(Vagon, on_delete=models.RESTRICT, null= True, blank = True)
    # en_vagon_codigo = models.CharField(max_length=16, null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_evento =  [('START', 'EMPIEZA'),
                        ('STOP', 'PARA'),
                        ('CIRC', 'CIRCULANDO'),
                        ('ALARM_TEMP', 'ALARMA_TEMPERATURA'),
                        ('ALARM_ACEL', 'ALARMA_ACELERACIONES'),
                        ('INIT_MANT', 'INICIO_MANTENIMIENTO'),
                        ('FIN_MANT', 'FIN_MANTENIMIENTO'),
                        ('CAMBIO', 'CAMBIO_ANCHO'),
                        ('BOGIE', 'CAMBIO_BOGIE'),
                        ('VAGON', 'CAMBIO_VAGÓN'),
                        ]
    evento = models.CharField(max_length=12, choices = opciones_evento, default = 'CIRC')
    alarma_temp = models.ForeignKey(AlarmaTemp, on_delete=models.RESTRICT, null= True, blank = True)
    alarma_aceleracion = models.ForeignKey(AlarmaAceleracion, on_delete=models.RESTRICT, null= True, blank = True)
    cambio = models.ForeignKey(Cambio, on_delete=models.RESTRICT, null= True, blank = True)
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.RESTRICT, null= True, blank = True)
    
    def __str__(self):
        return (str(self.eje.codigo) + '-' + str(self.timestamp))
    def get_absolute_url(self):
        if self.evento == 'ALARM_TEMP':
            if self.alarma_temp.pk:
                return reverse("alarma_temperatura", kwargs={'pk':self.alarma_temp.pk})
            else:
                return ''
        elif self.evento == 'ALARM_ACEL':
            if self.alarma_aceleracion.pk:
                return reverse("alarma_aceleracion", kwargs={'pk':self.alarma_aceleracion.pk})
            else:
                return ''
        elif self.evento == 'CAMBIO':
            if self.cambio.pk:
                return reverse("ficha_cambio", kwargs={'pk':self.cambio.pk})
            else:
                return ''
        elif (self.evento == 'INIT_MANT' or self.evento == 'FIN_MANT'):
            if self.mantenimiento.pk:
                return reverse("ficha_mantenimiento", kwargs={'pk':self.mantenimiento.pk})
            else:
                return ''
        else:
            return ''

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


