# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from Aplications.orgtecol.models import Region, Departamento, Municipio
import json

from . import factories


# Create your tests here...
class OrgtecolTest(TestCase):
    def setUp(self):
        self.client = Client()
        _ = User.objects.create_user('usertemp', 'usertemp@mail.com', 'u123temp')

        reg_test = factories.RegionFactory.create()
        dep_test = Departamento.objects.create(reg=reg_test, depto_codigodane=05, depto_iso='DTEST',
                                               depto_nombre='dep_test')
        _ = Municipio.objects.create(depto=dep_test, mun_nombre='mun_test')

    # TEST VIEW QUE BUSCA DEARTAMENTOS QUE CONTENGAN STRINGS Y RETORNA JSON
    def test_view_depto_query_string_json(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/orgtecol/depto_query_string_json', {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(len(result['results']), 1)
        self.assertIs(result['success'], True)
        self.client.logout()

    # TEST VIEW QUE BUSCA MUNICIPIOS QUE CONTENGAN STRINGS Y RETORNA JSON
    def test_view_mun_query_string_json(self):
        self.client.login(username='usertemp', password='u123temp')
        response = self.client.get('/orgtecol/mun_query_string_json', {'query': 'mun_test'})
        self.assertEqual(response.status_code, 200)  # VERIFICANDO ESTADO DE LA RESPUESTA 200 OK
        result = json.loads(response.content)
        self.assertEqual(len(result['results']), 1)  # VERIFICANDO CANTIDAD DE RESULTADOS
        self.assertIs(result['success'], True)  # VERIFICANDO SI
        self.client.logout()
