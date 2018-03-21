# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.
class LandingPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('usertemp', 'usertemp@mail.com', 'u123temp')


    # TEST TEMPLATE LOGIN
    def test_template_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    # TEST DE FUNCIÓN LOGIN
    def test_login_user(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/', follow=True)
        user = User.objects.get(username='usertemp')
        self.assertEqual(user.email, 'usertemp@mail.com')


    # TEST INDEX DASHBOARD (REQUIERE ACUTENTICACIÓN DE USUARIO)
    def test_template_dashboard(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/dashboard/index')
        self.assertEqual(response.status_code, 200)


    # TEST TEMPLATE MAPA INTERACTIVO
    def test_template_mapainteractivo(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/dashboard/mapainteractivo')
        self.assertEqual(response.status_code, 200)

