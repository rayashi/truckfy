from django.contrib import admin
from apps.reviews.models import *


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'truck', 'client', 'rate', 'created_at')
    search_fields = ['id', 'truck.name']

admin.site.register(Review, ReviewAdmin)


