from django.contrib import admin
from apps.menu.models import *


class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    search_fields = ['id', 'name', 'truck.name']
    list_filter = ('truck',)

admin.site.register(Dish, DishAdmin)

