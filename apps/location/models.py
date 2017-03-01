from django.db import models


class CheckIn(models.Model):
    truck = models.ForeignKey('personas.Truck')
    latitude = models.CharField(max_length=50, blank=True, null=True, default=None)
    longitude = models.CharField(max_length=50, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'CheckIns'

    def __str__(self):
        return self.truck.name
