# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.
class SueloTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('usertemp', 'usertemp@mail.com', 'u123temp')

    # TEST TEMPLATE SUELO INDEX
    def test_template_index(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/suelo/index')
        self.assertEqual(response.status_code, 200)