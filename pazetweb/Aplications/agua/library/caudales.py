# -*- coding: utf-8 -*-
from django.db import connection, transaction
from datetime import *


class Caudales(object):

	# GENERA LA CURVA DE DURACIÓN DE CAUDAL PARA UNA ESTACIÓN
	def curva_duracion_caudal_convencional(self, codigo):

		cursor = connection.cursor()
		query = '''select caudi_fecha_reporte, caudi_caudal, row_number() OVER(order by caudi_caudal desc) as enumeracion 
		from general.caudal_diario where estn_codigo = %s and extract(year from caudi_fecha_reporte) in (
		select (extract(year from ag.caudi_fecha_reporte)) as anios from general.caudal_diario as ag
		where ag.estn_codigo=%s GROUP BY (extract(year from ag.caudi_fecha_reporte)) 
		having count(ag.caudi_caudal)>=((365*90)/100) ORDER BY anios) ORDER BY caudi_caudal desc'''

		cursor.execute(query, [codigo, codigo])

		columns = [x.name for x in cursor.description]
		caudales = cursor.fetchall()
		total = len(caudales)

		listCaudales, listAnios, listProb = [], [], []

		for caudal in caudales:
			row = dict(zip(columns, caudal))

			listCaudales.append(float(row['caudi_caudal']))

			listProb.append("%.3f" % ((float(row['enumeracion']) / (float(total) + 1)) * 100))

			auxanio = row['caudi_fecha_reporte'].strftime("%Y")
			if auxanio not in listAnios:
				listAnios.append(auxanio)

		listAnios.sort()  # SE ORDENA LA LISTA DE AÑOS

		adf =  sum(listCaudales) / float(len(listCaudales)) # CONSTANTE

		return listCaudales, listProb, listAnios, adf

	# LA ESTANDARIZACION POR ADF TRATA DE LA DIVICION DE CADA CAUDAL POR LA CONSTANTE ADF
	def estandarizacion_por_adf(self, listCaudales, adf):

		listCauEst = list(map((lambda x: "%.3f" % (x/adf)), listCaudales))

		return listCauEst
