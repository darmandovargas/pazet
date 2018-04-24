# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render

#from Aplications.GeoTools import config
#from Aplications.GeoTools.layercreate import LayerCreate
#from Aplications.GeoTools.thiessen import Thiessen
from Aplications.suelo.models import SueloPerfil, SueloMuestra, SueloMetalesPesados


# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/suelo/index.html', {})


@login_required
def thiessen(request):


    # if request.method == "POST":
    #
    #     listlatlng, data = [], []
    #
    #     muestras = SueloMuestra.objects.filter(mues_id__icontains='ZULIA')
    #     for muestra in muestras:
    #         listlatlng.append((muestra.mues_lng,muestra.mues_lat));
    #
    #     qgs = config.run()
    #     #pl = LayerCreate()
    #     #pointlayer = pl.LayerPoint(listlatlng, data)
    #
    #     tie = Thiessen()
    #     tie.voronoi()
    #     config.stop(qgs)

    return render(request, 'dashboard/suelo/thiessen.html', {})

@login_required
def interpolacion(request):
    return render(request, 'dashboard/suelo/interpolacion.html',{})

# ---------------------------------------------------------------------------------------
# ----------------------------------- JSON ----------------------------------------------
# ---------------------------------------------------------------------------------------

# OPTIENE LAS MUESTRAS DE UN PERFIL
def muestras_perfil_with_code_json(request):
    codigo = request.GET.get('codigo', None)

    try:
        perfil = SueloPerfil.objects.get(perf_codigo=codigo)
    except SueloPerfil.DoesNotExist:
        raise Http404("El perfil no éxiste")

    data = {
        'estudio': perfil.estu.estu_nombre,
        'publicacion': perfil.estu.estu_publicacion,
        'niveldetalle': perfil.estu.estu_nivel_detalle,
        'escala': perfil.estu.estu_escala,
        'depto_nombre': perfil.estu.depto.depto_nombre,
        'depto_iso': perfil.estu.depto.depto_iso,
        'perfil': perfil.perf_codigo,
        'codigo': perfil.perf_codigo,
        'latitud': perfil.perf_lng,
        'longitud': perfil.perf_lat,
    }

    cursor = connection.cursor()
    query = '''select * from general.view_all_muestras where perf_codigo = %s order by mues_prof_inicio, mues_prof_final'''
    print query
    cursor.execute(query, [codigo])
    columns = [x.name for x in cursor.description]
    muestras = cursor.fetchall()
    print columns
    print muestras
    json_data = json.dumps({'perfil': data, 'muestras': [dict(zip(columns, muestra)) for muestra in muestras]})
    return HttpResponse(json_data, content_type="application/json")


# OPTIENE LA INFORMACION DE UNA MUESTRA ESPESIFICA
def muestra_with_muesid_json(request):
    muesid = request.GET.get('muesid', None)

    cursor = connection.cursor()
    query = '''select * from general.view_all_muestras where mues_id = %s'''
    cursor.execute(query, [muesid])
    columns = [x.name for x in cursor.description]
    muestra = cursor.fetchone()
    print columns
    print "-----"
    print muestra
    json_data = json.dumps({'muestra': dict(zip(columns, muestra))})
    return HttpResponse(json_data, content_type="application/json")


def variables_prop_metales_pesados_json(request):

    excepciones = ['interp', 'smp_id', 'mues', 'smp_created', 'smp_updated']
    #lista_variables = [
    #    (f.name,f.verbose_name) for f in SueloMetalesPesados._meta.get_fields() if all(substr not in f.name for substr in excepciones)
    #]

    lista_variables = []
    for f in SueloMetalesPesados._meta.get_fields():
        if all(substr not in f.name for substr in excepciones):
            lista_variables.append({'text':f.verbose_name, 'value':f.name})


    return JsonResponse(lista_variables, safe=False)

# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------

def all_perfiles_geojson(request):
    response = []

    estaciones = cache.get('all_perfiles')

    if not estaciones:

        cursor = connection.cursor()
        query = '''select perf.perf_codigo, st_y(perf.perf_coordenadas) as perf_lat, 
		st_x(perf.perf_coordenadas) as perf_lng, estu.*, depto.depto_nombre, depto.depto_iso
		from general.suelo_perfil as perf join "general".suelo_estudio as estu on (estu.estu_id=perf.estu_id) 
		join general.orgtecol_departamento as depto on (depto.depto_codigodane=estu.depto_codigodane)'''

        cursor.execute(query)
        columns = [x.name for x in cursor.description]
        estaciones = cursor.fetchall()

        for estacion in estaciones:
            row = dict(zip(columns, estacion))
            response.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [row['perf_lng'], row['perf_lat']]},
                'properties': {
                    'codigo': row['perf_codigo'],
                    'estudio': row['estu_nombre'],
                    'pub': row['estu_publicacion'],
                    'depto_nombre': row['depto_nombre'],
                    'lat': row['perf_lat'],
                    'lng': row['perf_lng']
                }
            })

        # lo cacheamos por 30 minutos
        cache.set('all_perfiles', response, 30)
    else:
        response = estaciones

    return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                         'features': response})


def all_muestras_geojson(request):
    response = []

    muestras = cache.get('all_muestras')

    if not muestras:

        cursor = connection.cursor()
        query = '''select mues_id, st_x(mues_coordenadas) as mues_lng, st_y(mues_coordenadas) as mues_lat  
				from general.suelo_muestra where perf_codigo is null'''

        cursor.execute(query)
        columns = [x.name for x in cursor.description]
        muestras = cursor.fetchall()

        for muestra in muestras:
            row = dict(zip(columns, muestra))
            response.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [row['mues_lng'], row['mues_lat']]},
                'properties': {
                    'muesid': row['mues_id'],
                    'lat': row['mues_lat'],
                    'lng': row['mues_lng']
                }
            })

        # lo cacheamos por 30 minutos
        cache.set('all_muestras', response, 30)
    else:
        response = muestras

    return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                         'features': response})
