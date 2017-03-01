# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = ('id', 'truck', 'name', 'price')
