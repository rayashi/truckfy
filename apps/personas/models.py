from django.db import models
from django.contrib.auth.models import User
from apps.personas.utils import *


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True, default=None)
    user = models.OneToOneField(User, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=client_path, max_length=200)
    pin = models.CharField(max_length=5, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name


class Truck(models.Model):
    name = models.CharField(max_length=200)
    onwer_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    phone = models.CharField(max_length=30, blank=True, null=True, default=None)
    user = models.OneToOneField(User, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=client_path, max_length=200)
    pin = models.CharField(max_length=5, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Food Trucks'

    def __str__(self):
        return self.name
