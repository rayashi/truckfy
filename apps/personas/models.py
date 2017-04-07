from django.db import models
from django.contrib.auth.models import User
from apps.personas.utils import *
from geopy.distance import distance
import pytz


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True, default=None)
    user = models.OneToOneField(User, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=client_path, max_length=200, blank=True, null=True, default=None)
    pin = models.CharField(max_length=5, blank=True, null=True, default=None)
    following = models.ManyToManyField('personas.Truck', blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    latitude = models.CharField(max_length=50, blank=True, null=True, default=None)
    longitude = models.CharField(max_length=50, blank=True, null=True, default=None)

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
    review_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    review_amount = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Food Trucks'

    def __str__(self):
        return self.name

    def get_distance(self, location):
        last_checkin = self.get_actived_checkin()
        if not last_checkin:
            return None
        truck_location = (float(last_checkin.latitude), float(last_checkin.longitude))
        if not location or not truck_location:
            return None
        return int(distance(location, truck_location).meters)

    def get_formatted_address(self):
        last_checkin = self.get_actived_checkin()
        if not last_checkin:
            return None
        return last_checkin.formatted_address

    def get_latitude(self):
        last_checkin = self.get_actived_checkin()
        if not last_checkin:
            return None
        return last_checkin.latitude

    def get_longitude(self):
        last_checkin = self.get_actived_checkin()
        if not last_checkin:
            return None
        return last_checkin.longitude

    def get_actived_checkin(self):
        now = pytz.datetime.datetime.now().astimezone(pytz.timezone('UTC'))
        limit_time = now - pytz.datetime.timedelta(hours=12)
        return self.checkin_set.filter(updated_at__gt=limit_time).order_by('created_at').last()
