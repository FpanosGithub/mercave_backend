from django.db import models
from django.urls import reverse
from material.models import Vagon, Bogie, Eje, Cambiador
from red_ferroviaria.models import PuntoRed

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EVENTOS. Son generados desde el análisis del streaming de datos
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
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE, null= True, blank = True)
    
    def get_absolute_url(self):
        return reverse("alarma_temperatura", kwargs={'pk':self.pk})

class AlarmaAceleracion(models.Model):
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE, null= True, blank = True)

    def get_absolute_url(self):
        return reverse("alarma_aceleracion", kwargs={'pk_alarma':self.pk})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EVENTO DE EJE
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class EventoEje(models.Model):
    dt = models.DateTimeField()
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    en_bogie = models.ForeignKey(Bogie, on_delete=models.RESTRICT, null= True, blank = True)
    en_vagon = models.ForeignKey(Vagon, on_delete=models.RESTRICT, null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_evento =  [('START', 'EMPIEZA'),
                        ('STOP', 'PARA'),
                        ('CIRC', 'CIRCULANDO'),
                        ('NUDO','NUDO'),
                        ('ALARM_TEMP', 'ALARMA_TEMPERATURA'),
                        ('ALARM_ACEL', 'ALARMA_ACELERACIONES'),
                        ('ALARM_CAMB', 'ALARMA_CAMBIO'),
                        ('INIT_MANT', 'INICIO_MANTENIMIENTO'),
                        ('FIN_MANT', 'FIN_MANTENIMIENTO'),
                        ('CAMBIO', 'CAMBIO_ANCHO'),
                        ]
    evento = models.CharField(max_length=12, choices = opciones_evento, default = 'CIRC')
    vel = models.FloatField(default=0, null= True, blank = True)
    tempa = models.FloatField(default=25, null= True, blank = True)
    tempb = models.FloatField(default=25, null= True, blank = True)
    cambio = models.ForeignKey(Cambio, on_delete=models.RESTRICT, null= True, blank = True)
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.RESTRICT, null= True, blank = True)
    
    def __str__(self):
        return ('Eje:' + str(self.eje.codigo) + '/' + str(self.evento) + '-' + str(self.dt))
    def get_absolute_url(self):
        return reverse("evento_eje", kwargs={'pk':self.pk})

class EventoVagon(models.Model):
    dt = models.DateTimeField()
    vagon = models.ForeignKey(Vagon, on_delete=models.CASCADE)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_evento =  [('START', 'EMPIEZA'),
                        ('STOP', 'PARA'),
                        ('CIRC', 'CIRCULANDO'),
                        ('NUDO','NUDO'),
                        ('ALARM_TEMP', 'ALARMA_TEMPERATURA'),
                        ('ALARM_ACEL', 'ALARMA_ACELERACIONES'),
                        ('INIT_MANT', 'INICIO_MANTENIMIENTO'),
                        ('FIN_MANT', 'FIN_MANTENIMIENTO'),
                        ('CAMBIO', 'CAMBIO_ANCHO'),
                        ]
    evento = models.CharField(max_length=12, choices = opciones_evento, default = 'CIRC')
    vel = models.FloatField(default=0, null= True, blank = True)
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.RESTRICT, null= True, blank = True)
    
    def __str__(self):
        return ('Vagón:' + str(self.vagon.codigo) + '/' + str(self.evento) + '-' + str(self.dt))
    def get_absolute_url(self):
        return reverse("evento_vagon", kwargs={'pk':self.pk})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


