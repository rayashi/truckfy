from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.personas.serializers import *


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_authenticated(request):
    truck = None
    client = None

    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response(status=422, data={'Please login first'})

    if client:
        response = {
            'userType': 'client',
            'truck': TruckModelSerializer(truck, many=False).data
        }
    elif truck:
        response = {
            'userType': 'truck',
            'truck': TruckModelSerializer(truck, many=False).data
        }
    else:
        return Response(status=422, data={'Please login first'})

    return Response(status=200, data=response)

