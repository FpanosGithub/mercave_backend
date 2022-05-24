from django.db import models
from django.urls import reverse

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
    nudo = models.BooleanField(default=False)
    linea = models.ForeignKey(Linea, on_delete=models.RESTRICT, null= True, blank = True)
    pkilometrico = models.FloatField(null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    def __str__(self):
        if self.codigo: return (str(self.codigo) + ' - ' + str(self.lng) + ':' + str(self.lat))
        else: return ''