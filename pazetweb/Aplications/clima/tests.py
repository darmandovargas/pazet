# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from Aplications.clima.models import ClimaEscenariosCc, ClimaCo2


# Create your tests here.
class ClimaTest(TestCase):

    def setUp(self):

        self.client = Client()
        user = User.objects.create_user('usertemp', 'usertemp@mail.com', 'u123temp')

        self.escenario1 = ClimaEscenariosCc.objects.create(escc_nombre='test1')
        self.escenario2 = ClimaEscenariosCc.objects.create(escc_nombre='test2')
        self.reporte1 = ClimaCo2.objects.create(escc=self.escenario1, cotwo_year=2017, cotwo_contenido=100)
        self.reporte2 = ClimaCo2.objects.create(escc=self.escenario2, cotwo_year=2015, cotwo_contenido=90)


    # TEST TEMPLATE CLIMA INDEX
    def test_template_index(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/clima/index')
        self.assertEqual(response.status_code, 200)


    # TEST CLIMA MONTH
    def test_template_clima_month(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/clima/clima_month')
        self.assertEqual(response.status_code, 200)


    # TEST TEMPLATE CLIMA DAY
    def test_template_clima_day(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/clima/clima_day')
        self.assertEqual(response.status_code, 200)


    # TEST TEMPLATE CLIMA DIOXDC
    def test_template_clima_dioxdc(self):
        self.client.login(username='usertemp', password='u123temp')
        escenarios = ClimaEscenariosCc.objects.all()
        response = self.client.get('/clima/dioxdc', {'escenarios':escenarios})
        self.assertEqual(response.status_code, 200)