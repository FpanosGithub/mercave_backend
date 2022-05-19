from django.contrib import admin

from .models import Organizacion, Diseñador, Fabricante, Mantenedor, Keeper, Operador, Aprovador, Certificador, LicenciaFabricacion

# Register your models here.
admin.site.register(Organizacion)
admin.site.register(Diseñador)
admin.site.register(Fabricante)
admin.site.register(Mantenedor)
admin.site.register(Keeper)
admin.site.register(Operador)
admin.site.register(Aprovador)
admin.site.register(Certificador)
admin.site.register(LicenciaFabricacion)