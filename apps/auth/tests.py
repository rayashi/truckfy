# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.personas.models import *


class UserAuthenticatedTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name='José', username="jose@truckfy.com", email="jose@truckfy.com", password="123")
        Token.objects.create(user=user)
        Truck.objects.create(name="Pizza", owner_name="José", email="jose@truckfy.com", user=user)

        user = User.objects.create_user(first_name='Abel', username="abel@truckfy.com", email="abel@truckfy.com",password="123")
        Token.objects.create(user=user)
        Client.objects.create(name="Abel", email="abel@truckfy.com", user=user)

    def test_client_authenticated(self):
        c = APIClient()
        client = Client.objects.get(id=1)
        token = Token.objects.get(user=client.user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.get('/user-authenticated', data={}, format='json')
        self.assertEqual(response.status_code, 200)
        print('-- > Get client authenticated is ok ..')



