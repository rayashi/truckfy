from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import datetime

from apps.personas.serializers import *
from apps.bill.models import *
from apps.shared.permission import *


@transaction.atomic
@api_view(['POST'])
def truck_register(request):
    try:
        name = request.data['name']
        owner_name = request.data['owner_name']
        email = request.data['email']
        phone = request.data['phone']
        password = request.data['password']
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'error': 'All fields are required (name, email, password, owner_name)'})

    if User.objects.filter(email=email).exists():
        return Response(status=422, data={'error': 'USED_EMAIL'})

    user = User.objects.create_user(first_name=get_first_name(owner_name),
                                    last_name=get_last_name(owner_name),
                                    username=email, email=email, password=password)

    truck = Truck.objects.create(name=name, email=email, phone=phone, owner_name=owner_name, user=user)
    token = Token.objects.get_or_create(user=user)

    try:
        trial_plan = Plan.objects.get(code='TRIAL')
        ends_at = datetime.date.today() + datetime.timedelta(trial_plan.length*365/12)
        Bill.objects.create(truck=truck, plan=trial_plan, price=trial_plan.price, paid=True, ends_at=ends_at)
    except Plan.DoesNotExist:
        pass

    return Response({'token': token[0].pk}, status=200)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTruck])
def truck_update(request):
    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a truck user'})
    try:
        truck.name = request.data['name']
    except (MultiValueDictKeyError, KeyError):
        pass
    try:
        truck.owner_name = request.data['owner_name']
    except (MultiValueDictKeyError, KeyError):
        pass
    try:
        truck.email = request.data['email']
        if not User.objects.filter(username=truck.email).exists():
            truck.user.email = truck.email
            truck.user.username = truck.user.email
            truck.user.save()
        else:
            return Response(status=422, data={'error': 'USED_EMAIL'})
    except (MultiValueDictKeyError, KeyError):
        pass
    try:
        truck.phone = request.data['phone']
    except (MultiValueDictKeyError, KeyError):
        pass

    truck.save()
    return Response(status=200, data=TruckModelSerializer(truck, many=False).data)


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
        return Response(status=422, data={'error': 'USED_EMAIL'})

    user = User.objects.create_user(first_name=get_first_name(name), last_name=get_last_name(name),
                                    username=email, email=email, password=password)

    Client.objects.create(name=name, email=email, user=user)
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token[0].pk}, status=200)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsClient])
def client_update(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a client user'})
    try:
        client.name = request.data['name']
    except (MultiValueDictKeyError, KeyError):
        pass
    try:
        client.email = request.data['email']
        if not User.objects.filter(username=client.email).exists():
            client.user.email = client.email
            client.user.username = client.user.email
            client.user.save()
        else:
            return Response(status=422, data={'error': 'USED_EMAIL'})
    except (MultiValueDictKeyError, KeyError):
        pass
    try:
        client.phone = request.data['phone']
    except (MultiValueDictKeyError, KeyError):
        pass
    client.save()
    return Response(status=200, data=ClientSerializer(client, many=False).data)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTruck])
def truck_image(request):
    try:
        truck = Truck.objects.get(user=request.user)
    except Truck.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a truck user'})
    try:
        file = request.FILES['file']
    except MultiValueDictKeyError:
        return Response(status=422, data={'error': 'File was not sent'})
    if truck.avatar:
        truck.avatar.delete()
    truck.avatar = file
    truck.save()
    return Response(status=200, data={'avatar': truck.avatar.url})


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsClient])
def client_image(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return Response(status=422, data={'Access denied, You are not a client user'})
    try:
        file = request.FILES['file']
    except MultiValueDictKeyError:
        return Response(status=422, data={'error': 'File was not sent'})
    if client.avatar:
        client.avatar.delete()
    client.avatar = file
    client.save()
    return Response(status=200, data={'avatar': client.avatar.url})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsClient])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsClient])
def list_following(request):
    try:
        client = Client.objects.get(user=request.user)
        following = TruckModelSerializer(client.following.all(), many=True).data
        return Response(status=200, data={'following': following})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})


@transaction.atomic()
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsClient])
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
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsClient])
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
