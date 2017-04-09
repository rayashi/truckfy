# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *


class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ('id', 'truck', 'latitude', 'longitude', 'formatted_address',
                  'expires_at', 'created_at', 'updated_at')
