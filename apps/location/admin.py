from django.contrib import admin
from apps.location.models import *


class CheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'truck', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ['id', 'truck.id', 'truck.name']


admin.site.register(CheckIn, CheckInAdmin)

