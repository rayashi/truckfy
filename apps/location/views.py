from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from operator import attrgetter
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
import googlemaps

from apps.personas.serializers import *
from apps.location.models import *


@transaction.atomic
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def truck_checkin(request):
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

    gmaps = googlemaps.Client(key='AIzaSyBXrCfiQP0GgAtqtzpmQzWqCwwLj9q4X_Q')
    gmaps_result = gmaps.reverse_geocode(latlng=(latitude, longitude), result_type='street_address')
    if gmaps_result:
        formatted_address = gmaps_result[0].get('formatted_address')
    else:
        formatted_address = None

    if CheckIn.objects.filter(truck=truck).exists():
        checkin = CheckIn.objects.filter(truck=truck)[0]
        checkin.latitude = latitude
        checkin.longitude = longitude
        checkin.formatted_address = formatted_address
        checkin.save()
    else:
        CheckIn.objects.create(truck=truck, latitude=latitude, longitude=longitude, formatted_address=formatted_address)
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

    if not request.user.is_anonymous():
        try:
            client = Client.objects.get(user=request.user)
            client.latitude = latitude
            client.longitude = longitude
            client.save()
        except Client.DoesNotExist:
            pass

    for truck in Truck.objects.all():
        truck.distance = truck.get_distance(location=location)
        truck.formatted_address = truck.get_formatted_address()
        truck.latitude = truck.get_latitude()
        truck.longitude = truck.get_longitude()
        if truck.distance == 0 or truck.distance:
            truck.distance = int(truck.distance)
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
