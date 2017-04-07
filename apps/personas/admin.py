from django.contrib import admin
from apps.personas.models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'avatar', 'created_at')
    search_fields = ['id', 'name']


class TruckAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'user', 'avatar', 'created_at')
    search_fields = ['id', 'name']


admin.site.register(Client, ClientAdmin)
admin.site.register(Truck, TruckAdmin)

