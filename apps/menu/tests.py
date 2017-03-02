# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.personas.models import *


class DishTestCase(TestCase):
    c = APIClient()

    def setUp(self):
        user = User.objects.create_user(first_name='José', username="jose@truckfy.com", email="jose@truckfy.com", password="123")
        Token.objects.create(user=user)
        Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)

    def test_truck_register(self):
        """Testa cadastro de prato"""
        truck = Truck.objects.get(id=1)
        token = Token.objects.get(user=truck.user)
        self.c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'truck': 1, 'name': 'Pizza de Calabreza', 'text': 'Boa qualidade de calabresa', 'price': 134.90}
        response = self.c.post('/dish/', data=data, format='json')
        self.assertEqual(response.json().get('name'), 'Pizza de Calabreza')

        print('-- > Dish add is ok ')
