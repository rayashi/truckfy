from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from operator import attrgetter
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
import googlemaps

from apps.personas.serializers import *
from apps.location.serializers import *


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

    try:
        duration = int(request.data['duration'])
    except (MultiValueDictKeyError, KeyError):
        duration = 6

    gmaps = googlemaps.Client(key='AIzaSyBXrCfiQP0GgAtqtzpmQzWqCwwLj9q4X_Q')
    gmaps_result = gmaps.reverse_geocode(latlng=(latitude, longitude), result_type='street_address')
    if gmaps_result:
        formatted_address = gmaps_result[0].get('formatted_address')
    else:
        formatted_address = None

    now = pytz.datetime.datetime.now().astimezone(pytz.timezone('UTC'))
    expires_at = now + pytz.datetime.timedelta(hours=duration)
    if CheckIn.objects.filter(truck=truck).exists():
        checkin = CheckIn.objects.filter(truck=truck)[0]
        checkin.latitude = latitude
        checkin.longitude = longitude
        checkin.formatted_address = formatted_address
        checkin.expires_at = expires_at
        checkin.save()
    else:
        CheckIn.objects.create(truck=truck, latitude=latitude, longitude=longitude,
                               formatted_address=formatted_address, expires_at=expires_at)
    return Response(status=200, data={'Check-in saved'})


@transaction.atomic
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def truck_checkout(request):
    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a truck user'})

    CheckIn.objects.filter(truck=truck).delete()
    return Response(status=200, data={'Check-out saved'})


@api_view(['GET'])
def actived_checkin(request):
    try:
        truck = Truck.objects.get(id=request.query_params['truck'])
        checkin = truck.get_actived_checkin()
        if checkin:
            response = CheckInSerializer(checkin, many=False).data
        else:
            response = False
        return Response(status=200, data=response)

    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'Truck is requered'})
    except Truck.DoesNotExist:
        return Response(status=422, data={'Truck does not exist'})


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
    open_trucks = []

    if not request.user.is_anonymous():
        try:
            client = Client.objects.get(user=request.user)
            client.latitude = latitude
            client.longitude = longitude
            client.save()
        except Client.DoesNotExist:
            pass

    for truck in Truck.objects.all().exclude(checkin__isnull=True).order_by('-review_rate'):
        truck.distance = truck.get_distance(location=location)
        truck.formatted_address = truck.get_formatted_address()
        truck.latitude = truck.get_latitude()
        truck.longitude = truck.get_longitude()
        if truck.distance == 0 or truck.distance:
            trucks.append(truck)
            open_trucks.append(truck.id)

    trucks.sort(key=attrgetter('distance'), reverse=False)

    for truck in Truck.objects.all().exclude(id__in=open_trucks).order_by('-review_rate'):
        truck.distance = None
        truck.formatted_address = None
        truck.latitude = None
        truck.longitude = None
        trucks.append(truck)

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
