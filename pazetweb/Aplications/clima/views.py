# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from Aplications.clima.models import ClimaCo2, ClimaEscenariosCc
import csv
import datetime
import unicodecsv as csv

# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/clima/index.html', {})


@login_required
def clima_month(request):
    return render(request, 'dashboard/clima/clima_month.html', {})


@login_required
def clima_day(request):
    return render(request, 'dashboard/clima/clima_day.html', {})


@login_required
def dioxdc(request):
    escenarios = ClimaEscenariosCc.objects.all()
    return render(request, 'dashboard/clima/dioxdc.html', {'escenarios':escenarios})


@login_required
def dioxdc_download(request, escenario_id):

    escenario = ClimaEscenariosCc.objects.get(pk=escenario_id);
    emisiones =  escenario.climaco2_set.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'inline; filename="escenario_cc_%s.csv"' % (escenario.escc_nombre.lower())
    writer = csv.writer(response)

    if emisiones:

        writer.writerow(['AÑO','EMISION'])

        for emision in emisiones:

            writer.writerow([ emision.cotwo_year, emision.cotwo_contenido ])
    else:
        writer.writerow(['Estacion/es sin datos en el rango de fecha seleccionado'])

    return response

    pass


@login_required
def clima_month_download_csv(request):

    listEstaciones = request.GET.getlist('estaciones')
    finicio = request.GET.get('first_date').split('-') # Ej: 1980-01
    ffinal = request.GET.get('second_date').split('-') # Ej: 2017-11

    # SE ELIMINAN LAS ESTACIONES REPETIDAS
    listCod = []
    [listCod.append(x) for x in listEstaciones if x not in listCod]

    # CONSULTA POSTGRESQL
    query = '''select * from general.clima_mensual where estn_codigo IN (%s)
        and (cmen_year, cmen_month) between (%s, %s) and (%s,%s) ORDER BY cmen_year, cmen_month''' \
        % (','.join("'%s'" % str(codigo) for codigo in listCod),finicio[0], finicio[1], ffinal[0],ffinal[1])

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    data = cursor.fetchall()

    # GENERACIÓN DE DOCUMENTO CSV
    response = None
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'inline; filename="clima_mensual.csv"'
    writer = csv.writer(response, encoding='utf-8')

    if data:

        writer.writerow(['#', 'ESTACION', 'AÑO', 'MES', 'PPT (mm)', 'Tm (°C)', 'Tn (°C)', 'Tx (°C)', 'HR (%)', 'BS'])

        for index, clima in enumerate(data):
            row = dict(zip(columns, clima))

            writer.writerow(
                [str(index + 1), row['estn_codigo'], str(row['cmen_year']), str(row['cmen_month']),
                 row['cmen_precipitacion'], row['cmen_temp_media'], row['cmen_temp_min'],
                 row['cmen_temp_max'], row['cmen_humedad_relativa'], row['cmen_brillo_solar']
                 ])
    else:
        writer.writerow(['Estacion/es sin datos en el rango de fecha seleccionado'])

    return response


@login_required
def clima_day_download_csv(request):
    listEstaciones = request.GET.getlist('estaciones')
    finicio = request.GET.get('first_date')
    ffinal = request.GET.get('second_date')

    # SE ELIMINAN LAS ESTACIONES REPETIDAS
    listCod = []
    [listCod.append(x) for x in listEstaciones if x not in listCod]

    fech_inicio = datetime.datetime.strptime(finicio, '%Y-%m-%d').date()
    fech_final = datetime.datetime.strptime(ffinal, '%Y-%m-%d').date()

    query = '''select * from general.clima_diario where estn_codigo IN (%s) and cdia_fecha_reporte 
        between('%s') and ('%s')''' % (','.join("'%s'" % str(codigo) for codigo in listCod), fech_inicio, fech_final)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    data = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'inline; filename="clima_diario.csv"'
    writer = csv.writer(response)

    if data:

        writer.writerow(
            ['#', 'ESTACION', 'FECHA', 'PPT (mm)', 'Tm (°C)', 'Tn (°C)', 'Tx (°C)', 'HR (%)', 'BS'])

        for index, clima in enumerate(data):
            row = dict(zip(columns, clima))

            writer.writerow([str(index + 1), row['estn_codigo'], str(row['cdia_fecha_reporte']),
                             row['cdia_precipitacion'],
                             row['cdia_temp_media'], row['cdia_temp_minima'],
                             row['cdia_temp_maxima'], row['cdia_humedad_relativa'], row['cdia_brillo_solar']
                             ])
    else:
        writer.writerow(['Estacion/es sin datos en el rango de fecha seleccionado'])

    return response



# **********************************************************************************************************************
# *********************************************** GRAFICAS (json) ******************************************************
# **********************************************************************************************************************

def emisiones_with_escenario_json(request):
    escenario_id = request.GET.get('escenario_id')
    escenario = ClimaEscenariosCc.objects.get(pk=escenario_id)
    emisiones = ClimaCo2.objects.filter(escc=escenario)

    yearemi, emisi = [], []

    for emision in emisiones:
        emisi.append(emision.cotwo_contenido)
        yearemi.append(emision.cotwo_year)

    return JsonResponse({'emisiones':emisi, 'yearemi':yearemi}, safe=False)


def clima_month_estn_year_json(request):

    codigo_estacion = request.GET.get('codigo', None)
    yearini = request.GET.get('anioini', None)

    query = '''select * from general.clima_mensual where estn_codigo='%s' and cmen_year = %s 
    ORDER BY cmen_year, cmen_month''' % (codigo_estacion, yearini)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    climas = cursor.fetchall()

    fecha, ppt, temp_med, temp_max, temp_min, hum, bs, datos = [], [], [], [], [], [], [], []

    for clima in climas:
        row = dict(zip(columns, clima))

        fdate = str(row['cmen_year']) + "-" + str(row['cmen_month'])

        fecha.append(fdate)
        ppt.append(row['cmen_precipitacion'] or None)
        temp_max.append(row['cmen_temp_max'] or None)
        temp_med.append(row['cmen_temp_media'] or None)
        temp_min.append(row['cmen_temp_min'] or None)
        hum.append(row['cmen_humedad_relativa'] or None)
        bs.append(row['cmen_brillo_solar'] or None)

        datos.append({
            'fecha': fdate, 'ppt': row['cmen_precipitacion'], 'temp_max': row['cmen_temp_max'],
            'temp_med': row['cmen_temp_media'], 'temp_min': row['cmen_temp_min'], 'hum': row['cmen_humedad_relativa'],
            'bs': row['cmen_brillo_solar']
        })

    data = {
        'fecha': fecha, 'ppt': ppt, 'temp_med':temp_med, 'temp_max':temp_max, 'temp_min':temp_min, 'hum':hum, 'bs':bs,
        'datos':datos
    }

    return JsonResponse(data, safe=False)


def clima_day_estn_year_json(request):

    codigo_estacion = request.GET.get('codigo', None)
    yearini = request.GET.get('anioini', None)

    query = '''select * from general.clima_diario where estn_codigo='%s' and 
    EXTRACT(year FROM cdia_fecha_reporte) = %s ORDER BY cdia_fecha_reporte''' % (codigo_estacion, yearini)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [x.name for x in cursor.description]
    climas = cursor.fetchall()

    fecha, ppt, temp_med, temp_max, temp_min, hum, bs, datos = [], [], [], [], [], [], [], []

    for clima in climas:
        row = dict(zip(columns, clima))

        fdate = str(row['cdia_fecha_reporte'])

        fecha.append(fdate)
        ppt.append(row['cdia_precipitacion'] or None)
        temp_med.append(row['cdia_temp_media'] or None)
        temp_max.append(row['cdia_temp_maxima'] or None)
        temp_min.append(row['cdia_temp_minima'] or None)
        hum.append(row['cdia_humedad_relativa'] or None)
        bs.append(row['cdia_brillo_solar'] or None)

        datos.append({
            'fecha': fdate, 'ppt': row['cdia_precipitacion'], 'temp_max': row['cdia_temp_maxima'],
            'temp_med': row['cdia_temp_media'], 'temp_min': row['cdia_temp_minima'], 'hum': row['cdia_humedad_relativa'],
            'bs': row['cdia_brillo_solar']
        })

    data = {
        'fecha': fecha, 'ppt': ppt, 'temp_med': temp_med, 'temp_max': temp_max, 'temp_min': temp_min, 'hum': hum,
        'bs': bs, 'datos': datos
    }
    return JsonResponse(data, safe=False)



