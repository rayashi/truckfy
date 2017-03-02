# -*- coding: utf-8 -*-
from django.db import transaction
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.personas.models import Truck
from apps.menu.serializers import *


@transaction.atomic
@api_view(['PUT'])
def create_dish(request):
    if request.user.is_anonymous():
        return Response(status=422, data={'Access denied, You are not a truck user'})

    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a truck user'})

    try:
        name = float(request.data['name'])
    except (MultiValueDictKeyError, TypeError):
        return Response(status=422, data={'Name is required'})

    try:
        text = float(request.data['text'])
    except (MultiValueDictKeyError, TypeError):
        text = None

    try:
        price = float(request.data['price'])
    except (MultiValueDictKeyError, TypeError):
        price = None

    dish = Dish.objects.create(name=name, text=text, price=price)
    return Response(status=200, data={'dish': DishSerializer(dish, many=False).data})

