from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.decorators import api_view
from operator import attrgetter
from django.db import transaction

from apps.personas.serializers import *
from apps.location.models import *


@transaction.atomic
@api_view(['POST'])
def truck_checkin(request):
    if request.user.is_anonymous():
        return Response(status=422, data={'Access denied, You are not a truck user'})

    try:
        latitude = float(request.data['latitude'])
        longitude = float(request.data['longitude'])
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a truck user'})
    except MultiValueDictKeyError:
        return Response(status=422, data={'Location is required'})
    except TypeError:
        return Response(status=422, data={'Please enter a valid location'})

    if CheckIn.objects.filter(truck=truck).exists():
        checkin = CheckIn.objects.filter(truck=truck)[0]
        checkin.latitude = latitude
        checkin.longitude = longitude
    else:
        CheckIn.objects.create(truck=truck, latitude=latitude, longitude=longitude)
    return Response(status=200, data={'Checkin saved'})


@api_view(['GET'])
def near_trucks(request):
    try:
        latitude = float(request.query_params['latitude'])
        longitude = float(request.query_params['longitude'])
        location = (latitude, longitude)
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'Latitude and longitude is requered'})

    page = request.GET.get('page')
    if not page:
        page = 1

    trucks = []

    for truck in Truck.objects.all():
        truck.distance = truck.get_distance(location=location)
        if truck.distance:
            trucks.append(truck)

    trucks.sort(key=attrgetter('distance'), reverse=False)
    paginator = Paginator(trucks, 10)

    try:
        near_trucks_pag = TruckSerializer(paginator.page(page), many=True).data
    except PageNotAnInteger:
        near_trucks_pag = TruckSerializer(paginator.page(1), many=True).data
    except EmptyPage:
        near_trucks_pag = []

    response = {
        'pages': paginator.num_pages,
        'page': int(page),
        'count': len(trucks),
        'neartrucks': near_trucks_pag
    }
    return Response(status=200, data=response)
