# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'avatar', 'email')


class TruckModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'name', 'avatar', 'owner_name', 'email', 'phone', 'created_at',
                  'review_rate', 'review_amount')


class TruckSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    avatar = serializers.ImageField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    distance = serializers.FloatField()
    formatted_address = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    review_rate = serializers.DecimalField(max_digits=10, decimal_places=1)
    review_amount = serializers.IntegerField()
