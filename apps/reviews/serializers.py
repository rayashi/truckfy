# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *

from apps.personas.serializers import *


class ReviewSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField()
    client = ClientSerializer()

    class Meta:
        model = Review
        fields = ('id', 'truck', 'client', 'rate', 'text', 'created_at')
