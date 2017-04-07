from django.db import models


class Plan(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Plano'

    def __str__(self):
        return self.name


class Bill(models.Model):
    truck = models.ForeignKey('personas.Truck')
    plan = models.ForeignKey('Plan')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    paid = models.BooleanField(default=False)
    link = models.URLField(default=None, blank=True, null=True)
    paid_at = models.DateTimeField(default=None, blank=True, null=True)
    ends_at = models.DateField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Fatura'

    def __str__(self):
        return self.truck.name
