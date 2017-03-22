# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.personas.models import *


class RegistersTestCase(TestCase):
    c = APIClient()

    def setUp(self):
        user = User.objects.create_user(first_name='José', username="jose@truckfy.com", email="jose@truckfy.com", password="123")
        Token.objects.create(user=user)
        truck1 = Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)
        user = User.objects.create_user(first_name='Maria', username="maria@truckfy.com", email="maria@truckfy.com", password="123")
        Token.objects.create(user=user)
        truck2 = Truck.objects.create(name="Pão", owner_name="Maria", email="maria@truckfy.com", user=user)

        user = User.objects.create_user(first_name='Abel', username="abel@truckfy.com", email="abel@truckfy.com",password="123")
        Token.objects.create(user=user)
        client = Client.objects.create(name="Abel", email="abel@truckfy.com", user=user)
        client.following.add(truck1)

    def test_is_folling(self):
        c1 = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c1.post('/review', data={'truck': 1, 'text': 'Muito bom', 'rate': 4}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > End point /review is ok')

