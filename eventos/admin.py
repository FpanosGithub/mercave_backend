from django.contrib import admin

from eventos.models import Cambio, EventoVagon, Mantenimiento, AlarmaCambio, AlarmaTemp, AlarmaAceleracion, EventoEje, EventoVagon

# Register your models here.
admin.site.register(Cambio)
admin.site.register(Mantenimiento)
admin.site.register(AlarmaCambio)
admin.site.register(AlarmaTemp)
admin.site.register(AlarmaAceleracion)
admin.site.register(EventoEje)
admin.site.register(EventoVagon)