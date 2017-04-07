from django.contrib import admin
from apps.bill.models import *


class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'length', 'price', 'created_at', 'updated_at')
    search_fields = ['id', 'code', 'name']


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'truck', 'plan', 'price', 'paid', 'link', 'paid_at', 'ends_at', 'created_at', 'updated_at')
    search_fields = ['id', 'truck.name', 'plan.name']


admin.site.register(Plan, PlanAdmin)
admin.site.register(Bill, BillAdmin)

