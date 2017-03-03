# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'avatar')


class TruckSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    avatar = serializers.ImageField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    distance = serializers.FloatField()

