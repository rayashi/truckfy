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
        truck = Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)
        truck.dish_set.create(name='Gorgonzola', text='Muito boa', price=43.9)
        truck.dish_set.create(name='Pimentão', text='Muito ruim', price=40.9)

        user = User.objects.create_user(first_name='José', username="pedro@truckfy.com", email="pedro@truckfy.com", password="123")
        Token.objects.create(user=user)
        truck = Truck.objects.create(name="Carne Truck", owner_name="pedro", email="pedro@truckfy.com", user=user)
        truck.dish_set.create(name='Picanha', text='Muito boa', price=3.9)
        truck.dish_set.create(name='Acem', text='Muito ruim', price=20.9)

    def test_dish_register(self):
        """Testa cadastro de prato"""
        truck = Truck.objects.get(id=1)
        token = Token.objects.get(user=truck.user)
        self.c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'truck': 1, 'name': 'Pizza de Calabreza', 'text': 'Boa qualidade de calabresa', 'price': 134.90}
        response = self.c.post('/dish/', data=data, format='json')
        self.assertEqual(response.json().get('name'), 'Pizza de Calabreza')
        print('-- > Dish add is ok ')

    def test_dish_filter(self):
        """Testa lista de pratos de um truck"""
        data = {'truck': 1}
        response = self.c.get('/dish/', data=data, format='json')
        self.assertEqual(len(response.json()), 2)
        print('-- > Dish list with filter work fine')
