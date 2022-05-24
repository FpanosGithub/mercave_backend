from django.db import models
from django.urls import reverse
from organizaciones.models import Operador, Fabricante, Mantenedor, Keeper
from ingenieria.models import VersionEje, VersionCambiador 

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Elementos del sistema Mercave / Activos físicos
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Aquí hay algo de locura. Las composiciones tienen vagones y estos a veces tienen bogies
# que llevan ejes y a veces no llevan bogies y los ejes van directamente a los vagones.
# la estructura de datos es flexible y se supone que las funciones que tengan que formar 
# composiciones, vagones, etc se encargarán e mantener todo coherentemente. ahora un eje 
# podría quedar asignado a un bogie y a un vagón que no van juntos.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Composicion(models.Model):
    codigo = models.CharField(max_length=20, unique= True)
    operador= models.ForeignKey(Operador, on_delete=models.CASCADE, null=True, blank=True)
    lng = models.FloatField(default=-3.9820) # grados
    lat = models.FloatField(default=40.2951) # grados
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_composicion", kwargs={'pk':self.pk})
    def mover(self, localizacion):
        self.lng = localizacion['lng']
        self.lat = localizacion['lat']
        self.save()

class Vagon(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    tipo = models.CharField(max_length=20,default = ' ')
    descripcion = models.CharField(max_length=100, default = ' ')
    num_bogies= models.IntegerField(default=2, null=True, blank=True)
    num_ejes = models.IntegerField(default=4, null=True, blank=True)
    foto = models.ImageField(upload_to='vagones/', blank = True)
    operador= models.ForeignKey(Operador, on_delete=models.RESTRICT, null=True, blank=True)
    keeper= models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    mantenedor= models.ForeignKey(Mantenedor, on_delete=models.RESTRICT, limit_choices_to={'de_vagones': True}, null=True, blank=True)
    composicion= models.ForeignKey(Composicion, on_delete=models.RESTRICT, null=True, blank=True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Variables de estado del vagón para gestionar los eventos de circulación
    transmitiendo = models.BooleanField(default=False)
    parado = models.BooleanField(default=True)
    alarma_temp = models.BooleanField(default=False)
    alarma_aceleraciones = models.BooleanField(default=False)
    ultimo_evento_dt = models.DateField(null=True, blank=True)
    ultimo_evento_circ = models.BooleanField(default=True)
    vel = models.FloatField(default=0, null=True, blank=True)
    lng = models.FloatField(default=-3.9820) # grados
    lat = models.FloatField(default=40.2951) # grados
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_vagon", kwargs={'pk':self.pk})
    # Funciones creadas para leer y guardar datos de las lógicas de negocio de logistica_feroviaria
    def composicion_posicionada(self, posicion):
        if self.composicion:
            if (self.composicion.lng == posicion['lng'] and self.composicion.lat == posicion['lat']):
                return True
            else:
                return False
        return True
    def mover(self, posicion):
        self.lng = posicion['lng']
        self.lat = posicion['lat']
        self.save()
    def desacoplar_de_composicion(self):
        self.composicion = None
        self.save()
    def acoplar_a_composicion(self, composicion):
        self.composicion = composicion
        self.save()

class Bogie(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    tipo = models.CharField(max_length=20,default = ' ')
    foto = models.ImageField(upload_to='bogies/', blank = True)
    operador= models.ForeignKey(Operador, on_delete=models.RESTRICT, null=True, blank=True)
    keeper= models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    mantenedor= models.ForeignKey(Mantenedor, on_delete=models.RESTRICT, limit_choices_to={'de_bogies': True},)
    vagon= models.ForeignKey(Vagon, on_delete=models.RESTRICT, null=True, blank=True)
    lng = models.FloatField(default=-3.9820) # grados
    lat = models.FloatField(default=40.2951) # grados
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_bogie", kwargs={'pk':self.pk})
    def mover(self, localizacion):
        self.lng = localizacion['lng']
        self.lat = localizacion['lat']
        self.save()
    def desacoplar_de_vagon(self):
        self.vagon = None
        self.save()
    def acoplar_a_vagon(self, vagon):
        self.vagon = vagon
        self.save()

class Eje(models.Model):
    codigo = models.CharField(max_length=10, unique= True)
    version= models.ForeignKey(VersionEje, on_delete=models.RESTRICT, null=True, blank=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.RESTRICT, limit_choices_to={'de_ejes': True},null=True, blank=True)
    keeper = models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    operador = models.ForeignKey(Operador, on_delete=models.RESTRICT, null=True, blank=True)
    mantenedor = models.ForeignKey(Mantenedor, on_delete=models.RESTRICT, null=True, blank=True)
    fecha_fab = models.DateField(null=True, blank=True)
    num_cambios = models.IntegerField(default=0)
    km = models.FloatField(default=0)         # km
    coef_trabajo = models.FloatField(default=0)
    bogie = models.ForeignKey(Bogie, on_delete=models.RESTRICT, null=True, blank=True)
    vagon = models.ForeignKey(Vagon, on_delete=models.RESTRICT, null=True, blank=True)
    estado = models.CharField(max_length=15, choices = [('CIRCULANDO','CIRCULANDO'),('PARADO','PARADO'),('MANTENIMIENTO','MANTENIMIENTO')], default = 'PARADO')
    alarma = models.BooleanField(default=False)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_eje", kwargs={'pk':self.pk})
    def mover(self, localizacion):
        self.lng = localizacion['lng']
        self.lat = localizacion['lat']
        self.save()
    def desacoplar_de_bogie(self):
        self.bogie = None
        self.save()
    def desacoplar_de_vagon(self):
        self.vagon = None
        self.save()
    def acoplar_a_bogie(self, bogie):
        self.bogie = bogie
        self.save()
    def acoplar_a_vagon(self, vagon):
        self.vagon = vagon
        self.save()

class Cambiador(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    nombre = models.CharField(max_length=100, default = 'Experimental-01')
    version= models.ForeignKey(VersionCambiador, on_delete=models.RESTRICT, null=True, blank=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True},null=True, blank=True)
    mantenedor = models.ForeignKey(Mantenedor, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True},null=True, blank=True)
    fecha_fab = models.DateField(null=True, blank=True)
    num_cambios = models.IntegerField(default=0)
    mantenimiento = models.CharField(max_length=16)
    lng = models.FloatField(default=-4.6920) # grados
    lat = models.FloatField(default=37.9246) # grados

    def __str__(self):
        return (str(self.codigo) + ': ' + str(self.nombre))
    def get_absolute_url(self):
        return reverse("ficha_cambiador", kwargs={'pk':self.pk})
