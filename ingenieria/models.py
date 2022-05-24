from django.db import models
from django.urls import reverse
from organizaciones.models import Fabricante, Diseñador, Aprovador, Certificador

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Modelos que representan la ingeniería de los elementos mercave / Activos inmateriales
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class VersionEje(models.Model):
    codigo= models.CharField(max_length=16, unique= True)
    opciones_anchos =  [('UIC-IB', 'UIC(1435) <> IBÉRICO (1668)'),
                        ('UIC-RUS', 'UIC(1435) <> RUSO (1520)'),
                        ('UIC-RUS-IB', 'UIC <> RUSO <> IBÉRICO'),
                        ('METR-UIC', 'MÉTRICO(1000) <> UIC(1435)'),]
    anchos = models.CharField(max_length=12, choices = opciones_anchos, default = 'UIC-IB')
    diseñador = models.ForeignKey(Diseñador, on_delete=models.RESTRICT, limit_choices_to={'de_ejes': True},)
    rueda = models.CharField(max_length=16)
    cuerpo_eje = models.CharField(max_length=16)
    aprovador = models.ForeignKey(Aprovador, on_delete=models.RESTRICT)
    fecha_aprovacion = models.DateField(null=True, blank=True)
    certificador = models.ForeignKey(Certificador, on_delete=models.RESTRICT)
    fecha_certificacion = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_version_eje", kwargs={'pk':self.pk})

class VersionCambiador(models.Model):
    codigo= models.CharField(max_length=16, unique= True)
    opciones_anchos =  [('UIC-IB', 'UIC(1435) <> IBÉRICO (1668)'),
                        ('UIC-RUS', 'UIC(1435) <> RUSO (1520)'),
                        ('METR-UIC', 'MÉTRICO(1000) <> UIC(1435)'),]
    anchos = models.CharField(max_length=12, choices = opciones_anchos, default = 'UIC-IB')
    diseñador = models.ForeignKey(Diseñador, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True},)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True}, null=True, blank=True)
    longitud_desencerrojado = models.FloatField(default=6000)   # mm
    longitud_cambio_rueda = models.FloatField(default=6000)     # mm
    longitud_encerrojado = models.FloatField(default=6000)      # mm
    longitud_total = models.FloatField(default = 36000)         # mm
    aprovador = models.ForeignKey(Aprovador, on_delete=models.RESTRICT)
    fecha_aprovacion = models.DateField(null=True, blank=True)
    certificador = models.ForeignKey(Certificador, on_delete=models.RESTRICT)
    fecha_certificacion = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_version_cambiador", kwargs={'pk':self.pk})
            