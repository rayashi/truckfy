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
        fields = ('id', 'name', 'avatar', 'owner_name', 'email', 'phone', 'created_at')


class TruckSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    avatar = serializers.ImageField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    distance = serializers.FloatField()

