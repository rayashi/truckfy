from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from apps.reviews.serializers import *
from apps.personas.models import *


@permission_classes((IsAuthenticated, ))
@transaction.atomic
@api_view(['POST'])
def review(request):

    try:
        text = request.data['text']
    except (MultiValueDictKeyError, KeyError):
        text = None

    try:
        rate = int(request.data['rate'])
        truck = Truck.objects.get(id=request.data['truck'])
        client = Client.objects.get(user=request.user)
        new_review = client.review_set.create(truck=truck, rate=rate, text=text)

        truck.review_amount += 1
        truck.review_rate = truck.review_set.all().aggregate(Avg('rate')).get('rate__avg')
        return Response(status=200, data={'review': ReviewSerializer(new_review, many=False).data})
    except Client.DoesNotExist:
        return Response(status=422, data={'error': 'You are not a client'})
    except Truck.DoesNotExist:
        return Response(status=422, data={'error': 'Truck does not exist'})
    except (MultiValueDictKeyError, KeyError):
        return Response(status=422, data={'error': 'Truck id and rate are required'})
