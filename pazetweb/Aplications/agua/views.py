# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from Aplications.agua.library.caudales import Caudales
import datetime
import csv
import unicodecsv as csv


# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/agua/index.html', {})


@login_required
def caudal_day(request):
    return render(request, 'dashboard/agua/caudal_day.html', {})


@login_required
def caudal_day_download_csv(request):
    listEstaciones = request.GET.getlist('estaciones')
    finicio = request.GET.get('first_date')
    ffinal = request.GET.get('second_date')

    # SE ELIMINAN LAS ESTACIONES REPETIDAS
    listCod = []
    [listCod.append(x) for x in listEstaciones if x not in listCod]

    fech_inicio = datetime.datetime.strptime(finicio, '%Y-%m-%d').date()
    fech_final = datetime.datetime.strptime(ffinal, '%Y-%m-%d').date()

    query = '''select * from general.caudal_diario where estn_codigo IN (%s) and caudi_fecha_reporte 
            between('%s') and ('%s')''' % (','.join("'%s'" % str(codigo) for codigo in listCod), fech_inicio, fech_final)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    data = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'inline; filename="caudal_diario.csv"'
    writer = csv.writer(response)

    if data:

        writer.writerow(['#', 'ESTACION', 'FECHA', 'CAUDAL (m3/s)'])

        for index, caudal in enumerate(data):
            row = dict(zip(columns, caudal))

            writer.writerow([ str(index + 1), row['estn_codigo'], row['caudi_fecha_reporte'], row['caudi_caudal'] ])
    else:
        writer.writerow(['Estacion/es sin datos en el rango de fecha seleccionado'])

    return response


# **********************************************************************************************************************
# *********************************************** GRAFICAS (json) ******************************************************
# **********************************************************************************************************************

@login_required
def caudal_day_estn_year_json(request):

    codigo_estacion = request.GET.get('codigo', None)
    yearini = request.GET.get('anioini', None)

    query = '''select * from general.caudal_diario where estn_codigo='%s' and 
    EXTRACT(year FROM caudi_fecha_reporte) = %s ORDER BY caudi_fecha_reporte''' % (codigo_estacion, yearini)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    caudales = cursor.fetchall()

    fecha, caud,  datos = [], [], []

    for caudal in caudales:
        row = dict(zip(columns, caudal))

        fdate = str(row['caudi_fecha_reporte'])

        fecha.append(fdate)
        caud.append(row['caudi_caudal'] or None)

        datos.append({
            'fecha': fdate, 'caudal': row['caudi_caudal']
        })

    data = { 'fecha': fecha, 'caudal': caud, 'datos': datos }

    return JsonResponse(data, safe=False)




#OPTIENE LA CURVA DE DURACIÓN DE CAUDAL DE UNA ESTACION POR SU CODIGO
@login_required
def cdc_diaria_estn_json(request):

    codigo_estacion = request.GET.get('codigo', None)

    curva = Caudales()
    listCaudal, listProb, listAnios, _ = curva.curva_duracion_caudal_convencional(codigo_estacion)
    # print (duracionCurva)

    return JsonResponse({'caudales': listCaudal, 'duracion': listProb, 'anios': listAnios}, safe=False)

