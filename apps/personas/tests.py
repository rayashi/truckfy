# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.personas.models import *
from apps.bill.models import *


class RegistersTestCase(TestCase):
    c = APIClient()

    def setUp(self):
        Plan.objects.create(code='TRIAL', name='Gratis 30 dias', length=1)
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

    def test_truck_register(self):
        """Testa cadastro do truck"""
        data = {'name': 'Pizza', 'owner_name': 'José', 'email': 'paulo@truckfy.com', 'phone':'349803215487', 'password': '1223'}
        response = self.c.post('/truck/register', data=data, format='json')
        self.assertEqual(response.status_code, 200)

        truck = Truck.objects.get(email='paulo@truckfy.com')
        token = Token.objects.get(user=truck.user).key
        self.assertEqual(response.json().get('token'), token)
        self.assertEqual(truck.bill_set.first().paid, True)
        print('-- > Truck register is ok, token = '+token)

    def test_client_register(self):
        """Testa cadastro do cliente"""
        data = {'name': 'José da Silva', 'email': 'monoel@truckfy.com', 'password': '1223'}
        response = self.c.post('/client/register', data=data, format='json')
        self.assertEqual(response.status_code, 200)

        truck = Client.objects.get(email='monoel@truckfy.com')
        token = Token.objects.get(user=truck.user).key
        self.assertEqual(response.json().get('token'), token)
        print('-- > Client register is ok, token = ' + token)

    def test_truck_list(self):
        """Testa busca da lista de truck"""
        response = self.c.get('/truck/', data={}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > Truck list is ok')

    def test_is_folling(self):
        c1 = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c1.get('/client/is-following', data={'truck':1}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > End point /client/is-following is ok')

    def test_list_following(self):
        c1 = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c1.get('/client/list-following', data={}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > End point /client/list-following is ok')

    def test_follow(self):
        c1 = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c1.post('/client/follow', data={'truck': 2}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > End point /client/follow is ok')

    def test_unfollow(self):
        c1 = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c1.post('/client/unfollow', data={'truck': 1}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > End point /client/unfollow is ok')
