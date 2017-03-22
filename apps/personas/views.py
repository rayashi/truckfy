from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from apps.personas.serializers import *
from apps.personas.utils import *


@transaction.atomic
@api_view(['POST'])
def truck_register(request):
    try:
        name = request.data['name']
        owner_name = request.data['owner_name']
        email = request.data['email']
        password = request.data['password']
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'error': 'All fields are required (name, email, password, owner_name)'})

    if User.objects.filter(email=email).exists():
        return Response(status=422, data={'error': 'Email used'})

    user = User.objects.create_user(first_name=get_first_name(owner_name),
                                    last_name=get_last_name(owner_name),
                                    username=email, email=email, password=password)

    Truck.objects.create(name=name, email=email, owner_name=owner_name, user=user)
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token[0].pk}, status=200)


@transaction.atomic
@api_view(['POST'])
def client_register(request):
    try:
        name = request.data['name']
        email = request.data['email']
        password = request.data['password']
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'error': 'All fields are required (name, email, password)'})

    if User.objects.filter(email=email).exists():
        return Response(status=422, data={'error': 'Email used'})

    user = User.objects.create_user(first_name=get_first_name(name), last_name=get_last_name(name),
                                    username=email, email=email, password=password)

    Client.objects.create(name=name, email=email, user=user)
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token[0].pk}, status=200)


@permission_classes((IsAuthenticated, ))
@transaction.atomic
@api_view(['POST'])
def truck_image(request):
    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Access denied, You are not a truck user'})

    if truck.avatar:
        truck.avatar.delete()

    truck.avatar = request.FILES['file']
    truck.save()
    return Response(status=200)


@permission_classes((IsAuthenticated, ))
@transaction.atomic
@api_view(['POST'])
def client_image(request):
    try:
        client = Client.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Access denied, You are not a client'})

    if client.avatar:
        client.avatar.delete()

    client.avatar = request.FILES['file']
    client.save()
    return Response(status=200)


@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def is_following(request):
    try:
        client = Client.objects.get(user=request.user)
        resp = client.following.filter(id=int(request.query_params['truck'])).exists()
        return Response(status=200, data={'is_following': resp})
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Truck does not exist'})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'Truck Id is required'})


@permission_classes((IsAuthenticated, ))
@api_view(['GET'])
def list_following(request):
    try:
        client = Client.objects.get(user=request.user)
        following = TruckModelSerializer(client.following.all(), many=True).data
        return Response(status=200, data={'following': following})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})


@transaction.atomic()
@permission_classes((IsAuthenticated, ))
@api_view(['POST'])
def follow(request):
    try:
        truck = int(request.data['truck'])
        client = Client.objects.get(user=request.user)
        client.following.add(truck)
        client.save()
        return Response(status=200, data={'following': True})
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Truck does not exist'})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'Truck Id is required'})


@transaction.atomic()
@permission_classes((IsAuthenticated, ))
@api_view(['POST'])
def unfollow(request):
    try:
        truck = int(request.data['truck'])
        client = Client.objects.get(user=request.user)
        client.following.remove(truck)
        client.save()
        return Response(status=200, data={'following': False})
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Truck does not exist'})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'Truck Id is required'})
