from django.contrib import admin

from eventos.models import Linea, PuntoRed, Cambio, Mantenimiento, AlarmaCambio, AlarmaTemp, AlarmaAceleracion, EventoEje

# Register your models here.
admin.site.register(Linea)
admin.site.register(PuntoRed)
admin.site.register(Cambio)
admin.site.register(Mantenimiento)
admin.site.register(AlarmaCambio)
admin.site.register(AlarmaTemp)
admin.site.register(AlarmaAceleracion)
admin.site.register(EventoEje)