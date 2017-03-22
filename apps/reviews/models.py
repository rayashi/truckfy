from django.db import models


class Review(models.Model):
    truck = models.ForeignKey('personas.Truck')
    client = models.ForeignKey('personas.Client')
    rate = models.IntegerField(default=5)
    text = models.TextField(max_length=600, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return str(self.rate)
