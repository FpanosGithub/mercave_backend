from django.contrib import admin

from material.models import Vagon, Bogie, Eje, Cambiador, Composicion

# Register your models here.

admin.site.register(Vagon)
admin.site.register(Bogie)
admin.site.register(Eje)
admin.site.register(Cambiador)
admin.site.register(Composicion)