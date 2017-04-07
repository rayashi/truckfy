# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.location.models import *
from apps.personas.models import *


class CheckInTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name='José', username="jose@truckfy.com", email="jose@truckfy.com", password="123")
        Token.objects.create(user=user)
        Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)

    def test_truck_checkin(self):
        """Testa se um truck pode fazer um checkin"""
        c = APIClient()
        truck = Truck.objects.get(id=1)
        token = Token.objects.get(user=truck.user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'latitude': '-18.920359', 'longitude': '-48.274231'}
        response = c.post('/checkin', data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CheckIn.objects.filter(truck=truck)[0].latitude, '-18.920359')
        self.assertEqual(CheckIn.objects.filter(truck=truck)[0].longitude, '-48.274231')

        response = c.get('/actived-checkin', data={'truck': truck.id})
        self.assertEqual(response.status_code, 200)

        response = c.post('/checkout')
        self.assertEqual(response.status_code, 200)
        print('-- > Truck Check-in and Check-out is ok ')


class NearTrucksTestCase(TestCase):
    c = APIClient()

    def setUp(self):
        user = User.objects.create_user(first_name='José', username="jose@truckfy.com", email="jose@truckfy.com", password="123")
        Token.objects.create(user=user)
        truck = Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)
        self.checkin(truck=truck, location=('-18.920359', '-48.274231'))
        user = User.objects.create_user(first_name='Maria', username="maria@truckfy.com", email="maria@truckfy.com", password="123")
        Token.objects.create(user=user)
        truck = Truck.objects.create(name="Pastel", owner_name="Maria", email="maria@truckfy.com", user=user)
        self.checkin(truck=truck, location=('-18.917177', '-48.270420'))
        user = User.objects.create_user(first_name='João', username="joao@truckfy.com", email="joao@truckfy.com", password="123")
        Token.objects.create(user=user)
        Truck.objects.create(name="Brigadeiro", owner_name="João", email="joao@truckfy.com", user=user)

    def test_near_trucks(self):
        """Testa busca por trucks"""
        response = self.c.get('/near-trucks', data={'latitude': '-18.919425', 'longitude': '-48.274735'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('neartrucks')[0].get('name'), 'Pizza')
        print('-- > Near trucks is ok, the first is '+response.json().get('neartrucks')[0].get('name'))

    def checkin(self, truck, location):
        token = Token.objects.get(user=truck.user)
        self.c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {'latitude': location[0], 'longitude': location[1]}
        response = self.c.post('/checkin', data=data, format='json')
        self.assertEqual(response.status_code, 200)
