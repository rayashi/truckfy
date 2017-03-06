from django.db import models
from django.contrib.auth.models import User
from apps.personas.utils import *
from geopy.distance import distance


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True, default=None)
    user = models.OneToOneField(User, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=client_path, max_length=200, blank=True, null=True, default=None)
    pin = models.CharField(max_length=5, blank=True, null=True, default=None)
    following = models.ManyToManyField('personas.Truck', blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name


class Truck(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    phone = models.CharField(max_length=30, blank=True, null=True, default=None)
    user = models.OneToOneField(User, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=truck_path, max_length=200, blank=True, null=True, default=None)
    pin = models.CharField(max_length=5, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Food Trucks'

    def __str__(self):
        return self.name

    def get_distance(self, location):
        if not self.checkin_set.all().exists():
            return None
        truck_location = (float(self.checkin_set.last().latitude), float(self.checkin_set.last().longitude))
        if not location or not truck_location:
            return None
        return distance(location, truck_location).meters

    def get_formatted_address(self):
        if not self.checkin_set.all().exists():
            return None
        return self.checkin_set.last().formatted_address

    def get_latitude(self):
        if not self.checkin_set.all().exists():
            return None
        return self.checkin_set.last().latitude

    def get_longitude(self):
        if not self.checkin_set.all().exists():
            return None
        return self.checkin_set.last().longitude
