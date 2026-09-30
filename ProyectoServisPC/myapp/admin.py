from django.contrib import admin
from .models import Cliente, Equipo,Tecnico, Reparacion, Opinion

# Register your models here.
admin.site.site_header = "Admin de ServisPC"
admin.site.site_title = "Panel de Administración de ServisPC"
admin.site.index_title = "Bienvenido al Panel de Administración de ServisPC"
admin.site.register(Cliente)
admin.site.register(Equipo)
admin.site.register(Tecnico)
admin.site.register(Reparacion)
admin.site.register(Opinion)