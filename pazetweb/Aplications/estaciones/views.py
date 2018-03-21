# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.estaciones.models import EstnEstacion
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.db import connection

# Create your views here.
# RENDERIZA LA VISTA PARA MOSTRAR LOS DATOS HISTORICOS DE UNA ESTACION
@login_required
def data_history(request, codigo):

	try:
		estacion = EstnEstacion.objects.get(estn_codigo=codigo)
	except EstnEstacion.DoesNotExist:
		raise Http404("OOPS! Código de estación invalido!")

	if estacion.clase.clase_siglas == 'MET':
		return render(request, 'dashboard/estacion/data_history_met.html', {'estacion': estacion})
	if estacion.clase.clase_siglas == 'HID':
		return render(request, 'dashboard/estacion/data_history_hid.html', {'estacion': estacion})
	if estacion.clase.clase_siglas == 'HMT':
		return render(request, 'dashboard/estaciones/data_history_hmt.html', {'estacion': estacion})






# ---------------------------------------------------------------------------------------
# ------------------------------------- JSON --------------------------------------------
# ---------------------------------------------------------------------------------------


# DEVUELVE LA INFORMACION DE UNA ESTACIÓN EN FORMATO JSON BUSCADA POR CODIGO DE LA ESTACION (CHEQUEADO)
def estacion_get_with_codigo(request):
	codigo = request.GET.get('codigo', None)

	cursor = connection.cursor()
	cursor.execute('''select * from general.view_all_estacion WHERE estn_codigo = %s''', [codigo])
	columns = [x.name for x in cursor.description]
	estacion = cursor.fetchone()

	data = dict(zip(columns, estacion))

	return JsonResponse(data, safe=False)


# **********************************************************************************************************************
# ************************************* FILTROS DE ESTACIONES CLIMA MENSUAL ********************************************
# **********************************************************************************************************************
# FILTRO DE ESTACIONES POR POLIGONO Y CLIMA MENSUAL
def filtro_estn_in_poligon_cmonth_json(request):

	tipo = request.GET.get('tipo', None)
	puntos = request.GET.getlist('puntos', None)
	radio = request.GET.get('radio', None)

	response = []

	if tipo == 'rectangle':

		punto1 = eval(puntos[0])
		punto2 = eval(puntos[2])

		query = '''select * from general.view_all_estacion where 
		st_contains((select ST_MakeEnvelope(%s, %s, %s, %s, 4326)), estn_coordenadas) 
		and estn_codigo in (select distinct estn_codigo as mensuales 
		from general.clima_mensual)''' % (punto1['lng'], punto1['lat'], punto2['lng'], punto2['lat'])

	elif tipo == 'circle':

		centro = eval(puntos[0])

		query = '''select * from general.view_all_estacion where 
				ST_Contains((select general.ST_Buffer_Meters((ST_SetSRID(ST_MakePoint(%s, %s),4326)), %s)), estn_coordenadas)
				and estn_codigo in (select distinct estn_codigo as mensuales 
				from general.clima_mensual)''' % (centro['lng'], centro['lat'], radio)

	elif tipo == 'polygon':

		poligono = ",".join(["%s %s" % (eval(punto)['lng'], eval(punto)['lat']) for punto in puntos]) + "," + str(
			eval(puntos[0])['lng']) + " " + str(eval(puntos[0])['lat'])

		query = '''select * from general.view_all_estacion 
						where ST_CONTAINS(ST_MakePolygon(ST_GeomFromText('SRID=4326;LINESTRING(%s)')), estn_coordenadas)
						and estn_codigo in (select distinct estn_codigo as mensuales 
						from general.clima_mensual)''' % (poligono)


	cursor = connection.cursor()
	cursor.execute(query)
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)

	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR DEPARTAMENTO Y CLIMA MENSUAL
def estn_clima_month_depto_json(request):

	codane = request.GET.get('codane', None)

	query = '''select * from general.view_all_estacion 
	where estn_codigo in (select distinct estn_codigo as mensuales from general.clima_mensual)
	and depto_codigodane = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [codane])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR MUNICIPIO Y CLIMA MENSUAL
def estn_clima_month_mun_json(request):
	munid = request.GET.get('munid', None)

	query = '''select * from general.view_all_estacion 
    	where estn_codigo in (select distinct estn_codigo as mensuales from general.clima_mensual)
    	and mun_id = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [munid])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR CODIGO DE ESTACION Y CLIMA MENSUAL
def estn_codigo_clima_month_json(request):
	codigo = request.GET.get('codigo', None)

	query = '''select * from general.view_all_estacion 
        	where estn_codigo in (select distinct estn_codigo as mensuales from general.clima_mensual)
        	and estn_codigo = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [codigo])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR PARTE DEL NOMBRE Y CLIMA MENSUAL
def estn_name_clima_month_json(request):
	nombre = request.GET.get('nombre', None)

	query = '''select * from general.view_all_estacion 
            	where estn_codigo in (select distinct estn_codigo as mensuales from general.clima_mensual)
            	and estn_nombre like %s '''

	cursor = connection.cursor()
	cursor.execute(query, ['%%' + nombre.upper() + '%%'])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)
# **********************************************************************************************************************


# **********************************************************************************************************************
# ************************************** FILTROS DE ESTACIONES CLIMA DIARIO ********************************************
# **********************************************************************************************************************
# FILTRO DE ESTACIONES POR POLIGONO Y CLIMA DIARIO
def filtro_estn_in_poligon_cday_json(request):

	tipo = request.GET.get('tipo', None)
	puntos = request.GET.getlist('puntos', None)
	radio = request.GET.get('radio', None)

	response = []

	if tipo == 'rectangle':

		punto1 = eval(puntos[0])
		punto2 = eval(puntos[2])

		query = '''select * from general.view_all_estacion where 
		st_contains((select ST_MakeEnvelope(%s, %s, %s, %s, 4326)), estn_coordenadas) 
		and estn_codigo in (select distinct estn_codigo as diarios 
		from general.clima_diario)''' % (punto1['lng'], punto1['lat'], punto2['lng'], punto2['lat'])

	elif tipo == 'circle':

		centro = eval(puntos[0])

		query = '''select * from general.view_all_estacion where 
				ST_Contains((select general.ST_Buffer_Meters((ST_SetSRID(ST_MakePoint(%s, %s),4326)), %s)), estn_coordenadas)
				and estn_codigo in (select distinct estn_codigo as diarios 
				from general.clima_diario)''' % (centro['lng'], centro['lat'], radio)

	elif tipo == 'polygon':

		poligono = ",".join(["%s %s" % (eval(punto)['lng'], eval(punto)['lat']) for punto in puntos]) + "," + str(
			eval(puntos[0])['lng']) + " " + str(eval(puntos[0])['lat'])

		query = '''select * from general.view_all_estacion 
						where ST_CONTAINS(ST_MakePolygon(ST_GeomFromText('SRID=4326;LINESTRING(%s)')), estn_coordenadas)
						and estn_codigo in (select distinct estn_codigo as diarios from general.clima_diario)''' % (poligono)


	cursor = connection.cursor()
	cursor.execute(query)
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)

	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR DEPARTAMENTO Y CLIMA DIARIO
def estn_clima_day_depto_json(request):

	codane = request.GET.get('codane', None)

	query = '''select * from general.view_all_estacion 
	where estn_codigo in (select distinct estn_codigo as diarios from general.clima_diario)
	and depto_codigodane = %s'''

	print query

	cursor = connection.cursor()
	cursor.execute(query, [codane])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR MUNICIPIO Y CLIMA DIARIO
def estn_clima_day_mun_json(request):
	munid = request.GET.get('munid', None)

	query = '''select * from general.view_all_estacion 
    	where estn_codigo in (select distinct estn_codigo as diarios from general.clima_diario)
    	and mun_id = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [munid])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR CODIGO DE ESTACION Y CLIMA DIARIO
def estn_codigo_clima_day_json(request):
	codigo = request.GET.get('codigo', None)

	query = '''select * from general.view_all_estacion 
        	where estn_codigo in (select distinct estn_codigo as diarios from general.clima_diario)
        	and estn_codigo = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [codigo])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR PARTE DEL NOMBRE Y CLIMA DIARIO
def estn_name_clima_day_json(request):
	nombre = request.GET.get('nombre', None)

	query = '''select * from general.view_all_estacion 
            	where estn_codigo in (select distinct estn_codigo as diarios from general.clima_diario)
            	and estn_nombre like %s '''

	cursor = connection.cursor()
	cursor.execute(query, ['%%' + nombre.upper() + '%%'])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)
# **********************************************************************************************************************


# **********************************************************************************************************************
# ************************************* FILTROS DE ESTACIONES CAUDAL DIARIO ********************************************
# **********************************************************************************************************************
# FILTRO DE ESTACIONES POR POLIGONO Y CAUDAL DIARIO
def filtro_estn_in_poligon_cauday_json(request):

	tipo = request.GET.get('tipo', None)
	puntos = request.GET.getlist('puntos', None)
	radio = request.GET.get('radio', None)

	response = []

	if tipo == 'rectangle':

		punto1 = eval(puntos[0])
		punto2 = eval(puntos[2])

		query = '''select * from general.view_all_estacion where 
		st_contains((select ST_MakeEnvelope(%s, %s, %s, %s, 4326)), estn_coordenadas) 
		and estn_codigo in (select distinct estn_codigo as diarios 
		from general.caudal_diario)''' % (punto1['lng'], punto1['lat'], punto2['lng'], punto2['lat'])

	elif tipo == 'circle':

		centro = eval(puntos[0])

		query = '''select * from general.view_all_estacion where 
				ST_Contains((select general.ST_Buffer_Meters((ST_SetSRID(ST_MakePoint(%s, %s),4326)), %s)), estn_coordenadas)
				and estn_codigo in (select distinct estn_codigo as diarios 
				from general.caudal_diario)''' % (centro['lng'], centro['lat'], radio)

	elif tipo == 'polygon':

		poligono = ",".join(["%s %s" % (eval(punto)['lng'], eval(punto)['lat']) for punto in puntos]) + "," + str(
			eval(puntos[0])['lng']) + " " + str(eval(puntos[0])['lat'])

		query = '''select * from general.view_all_estacion 
						where ST_CONTAINS(ST_MakePolygon(ST_GeomFromText('SRID=4326;LINESTRING(%s)')), estn_coordenadas)
						and estn_codigo in (select distinct estn_codigo as diarios from general.caudal_diario)''' % (poligono)


	cursor = connection.cursor()
	cursor.execute(query)
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)

	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR DEPARTAMENTO Y CAUDAL DIARIO
def estn_caudal_day_depto_json(request):

	codane = request.GET.get('codane', None)

	query = '''select * from general.view_all_estacion 
	where estn_codigo in (select distinct estn_codigo as diarios from general.caudal_diario)
	and depto_codigodane = %s'''

	print query

	cursor = connection.cursor()
	cursor.execute(query, [codane])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR MUNICIPIO Y CAUDAL DIARIO
def estn_caudal_day_mun_json(request):
	munid = request.GET.get('munid', None)

	query = '''select * from general.view_all_estacion 
    	where estn_codigo in (select distinct estn_codigo as diarios from general.caudal_diario)
    	and mun_id = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [munid])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR CODIGO DE ESTACION Y CAUDAL DIARIO
def estn_codigo_caudal_day_json(request):
	codigo = request.GET.get('codigo', None)

	query = '''select * from general.view_all_estacion 
        	where estn_codigo in (select distinct estn_codigo as diarios from general.caudal_diario)
        	and estn_codigo = %s'''

	cursor = connection.cursor()
	cursor.execute(query, [codigo])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)

# FILTRO DE ESTACIONES POR PARTE DEL NOMBRE Y CAUDAL DIARIO
def estn_name_caudal_day_json(request):
	nombre = request.GET.get('nombre', None)

	query = '''select * from general.view_all_estacion 
            	where estn_codigo in (select distinct estn_codigo as diarios from general.caudal_diario)
            	and estn_nombre like %s '''

	cursor = connection.cursor()
	cursor.execute(query, ['%%' + nombre.upper() + '%%'])
	columns = [x.name for x in cursor.description]
	estaciones = cursor.fetchall()

	response = []
	for estacion in estaciones:
		row = dict(zip(columns, estacion))
		response.append(row)
	return JsonResponse(response, safe=False)
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- GEOJSON ----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# TODAS LAS ESTACIONES QUE CONTIENEN INFORMACION
def all_stations_geojson(request):
	response = []

	estaciones = cache.get('estaciones_data')

	if not estaciones:

		cursor = connection.cursor()
		query = '''SELECT DISTINCT * FROM general.view_all_estacion WHERE 
				(estn_codigo IN ( SELECT DISTINCT estn_codigo FROM general.clima_mensual)) OR
				(estn_codigo IN ( SELECT DISTINCT estn_codigo FROM general.clima_diario)) OR
				(estn_codigo IN ( SELECT DISTINCT estn_codigo FROM general.caudal_diario))'''

		cursor.execute(query)
		columns = [x.name for x in cursor.description]
		estaciones = cursor.fetchall()

		for estacion in estaciones:
			row = dict(zip(columns, estacion))
			response.append({
				'type': 'Feature',
				'geometry': {'type': 'Point', 'coordinates': [row['estn_lng'], row['estn_lat']]},
				'properties': {'id': row['estn_codigo'], 'name': row['estn_nombre'] + ' [' + row['estn_codigo'] + ']',
							   'codigo': row['estn_codigo'], 'estado': row['estn_estado'],
							   'propietario': row['entds_siglas'], 'clase': row['clase_siglas'], 'lat': row['estn_lat'],
							   'lng': row['estn_lng']}
			})

		# lo cacheamos por 30 minutos
		cache.set('estaciones_data', response, 60)
	else:
		response = estaciones

	return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
						 'features': response})

# ESTACIONES CON VARIABLES CLIMATICAS MENSUALES
def all_estn_clima_month_geojson(request):
	response = []

	estaciones = cache.get('estaciones_month')

	if not estaciones:

		cursor = connection.cursor()
		query = '''select estn.estn_codigo, estn.estn_nombre, st_y(estn.estn_coordenadas) as estn_lat, 
					st_x(estn.estn_coordenadas) as estn_lng from general.estn_estacion as estn where estn.estn_codigo in 
					(select distinct estn_codigo as mensuales from general.clima_mensual)'''

		cursor.execute(query)
		columns = [x.name for x in cursor.description]
		estaciones = cursor.fetchall()

		for estacion in estaciones:
			row = dict(zip(columns, estacion))
			response.append({
				'type': 'Feature',
				'geometry': {'type': 'Point', 'coordinates': [row['estn_lng'], row['estn_lat']]},
				'properties': {'id': row['estn_codigo'], 'name': row['estn_nombre'] + ' [' + row['estn_codigo'] + ']',
							   'codigo': row['estn_codigo'], 'lat': row['estn_lat'],'lng': row['estn_lng']}
			})

		# lo cacheamos por 30 minutos
		cache.set('estaciones_month', response, 60)
	else:
		response = estaciones

	return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
						 'features': response})

# ESTACIONES CON VARIABLES CLIMATICAS DIARIAS
def all_estn_clima_day_geojson(request):
	response = []

	estaciones = cache.get('estaciones_day')

	if not estaciones:

		cursor = connection.cursor()
		query = '''select estn.estn_codigo, estn.estn_nombre, st_y(estn.estn_coordenadas) as estn_lat, 
					st_x(estn.estn_coordenadas) as estn_lng from general.estn_estacion as estn where estn.estn_codigo in 
					(select distinct estn_codigo as diarios from general.clima_diario)'''

		cursor.execute(query)
		columns = [x.name for x in cursor.description]
		estaciones = cursor.fetchall()

		for estacion in estaciones:
			row = dict(zip(columns, estacion))
			response.append({
				'type': 'Feature',
				'geometry': {'type': 'Point', 'coordinates': [row['estn_lng'], row['estn_lat']]},
				'properties': {'id': row['estn_codigo'], 'name': row['estn_nombre'] + ' [' + row['estn_codigo'] + ']',
							   'codigo': row['estn_codigo'], 'lat': row['estn_lat'],'lng': row['estn_lng']}
			})

		# lo cacheamos por 30 minutos
		cache.set('estaciones_day', response, 60)
	else:
		response = estaciones

	return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
						 'features': response})

# ESTACIONES CON CAUDALES DIARIOS
def all_estn_caudal_diario_geojson(request):
	response = []

	estaciones = cache.get('estaciones_cauday')

	if not estaciones:

		cursor = connection.cursor()
		query = '''select estn.estn_codigo, estn.estn_nombre, st_y(estn.estn_coordenadas) as estn_lat, 
    					st_x(estn.estn_coordenadas) as estn_lng from general.estn_estacion as estn where estn.estn_codigo in 
    					(select distinct estn_codigo as diarios from general.caudal_diario)'''

		cursor.execute(query)
		columns = [x.name for x in cursor.description]
		estaciones = cursor.fetchall()

		for estacion in estaciones:
			row = dict(zip(columns, estacion))
			response.append({
				'type': 'Feature',
				'geometry': {'type': 'Point', 'coordinates': [row['estn_lng'], row['estn_lat']]},
				'properties': {'id': row['estn_codigo'], 'name': row['estn_nombre'] + ' [' + row['estn_codigo'] + ']',
							   'codigo': row['estn_codigo'], 'lat': row['estn_lat'], 'lng': row['estn_lng']}
			})

		# lo cacheamos por 30 minutos
		cache.set('estaciones_cauday', response, 60)
	else:
		response = estaciones

	return JsonResponse({'type': 'FeatureCollection', 'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
						 'features': response})