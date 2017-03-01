from django.db import models


class Dish(models.Model):
    truck = models.ForeignKey('personas.Truck')
    name = models.CharField(max_length=200)
    text = models.TextField(max_length=600, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Pratos'

    def __str__(self):
        return self.name
