# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.personas.models import *


class RegistersTestCase(TestCase):
    c = APIClient()

    def setUp(self):
        pass

    def test_truck_register(self):
        """Testa cadastro do truck"""
        data = {'name': 'Pizza', 'owner_name': 'José', 'email': 'jose@truckfy.com', 'password': '1223'}
        response = self.c.post('/truck/register', data=data, format='json')
        self.assertEqual(response.status_code, 200)

        truck = Truck.objects.get(email='jose@truckfy.com')
        token = Token.objects.get(user=truck.user).key
        self.assertEqual(response.json().get('token'), token)
        print('-- > Truck register is ok, token = '+token)

    def test_client_register(self):
        """Testa cadastro do cliente"""
        data = {'name': 'José da Silva', 'email': 'jose@truckfy.com', 'password': '1223'}
        response = self.c.post('/client/register', data=data, format='json')
        self.assertEqual(response.status_code, 200)

        truck = Client.objects.get(email='jose@truckfy.com')
        token = Token.objects.get(user=truck.user).key
        self.assertEqual(response.json().get('token'), token)
        print('-- > Client register is ok, token = ' + token)
