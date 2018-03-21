# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.orgtecol.models import *
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.







# ---------------------------------------------------------------------------------------
# ------------------------------------- JSON --------------------------------------------
# ---------------------------------------------------------------------------------------
def mun_query_string_json(request):
    response = []
    if request.GET.get('query'):
        parametro = request.GET.get('query')

        municipios = Municipio.objects.filter(mun_nombre__icontains=parametro)[:5]
        for municipio in municipios:
            response.append({
                "name": municipio.mun_nombre + " (" + municipio.depto.depto_iso + ")",
                "value": municipio.mun_id,
                "text": municipio.mun_nombre + " (" + municipio.depto.depto_iso + ")",
            })
    return JsonResponse({'success': True, 'results': response})


def depto_query_string_json(request):
    response = []
    if request.GET.get('query'):
        parametro = request.GET.get('query')

        departamentos = Departamento.objects.filter(depto_nombre__icontains=parametro)[:5]
        for departamento in departamentos:
            response.append({
                "name": departamento.depto_nombre + " (" + departamento.depto_iso + ")",
                "value": departamento.depto_codigodane,
                "text": departamento.depto_nombre + " (" + departamento.depto_iso + ")",
            })
    return JsonResponse({'success': True, 'results': response})