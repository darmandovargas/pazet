# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from xhtml2pdf import pisa

# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Command(BaseCommand):
	help = "Create backup of database"
	args = "No necesita"  # NOMBRE DE LA CONFIGURACION DE LA BASE DE DATOS

	def handle(self, *args, **options):

		SCHEMA = 'general'

		print "Inicio"
		print "Espere"

		sourceHTML ="<!DOCTYPE html>"
		sourceHTML +="<html>"
		sourceHTML +="<body>"
		sourceHTML +=" <h2>Diccionario de datos</h2>"
		sourceHTML +="<h3>Base de Datos Agroclimatica Integral (BDAI)</h3>"
		sourceHTML +="<p>"
		sourceHTML +="A continuación se presenta el diccionario de datos representativo de la BASE DE DATOS AGROCLIMATICA INTEGRAL (BDAI)"
		sourceHTML +="</p>"
		sourceHTML +="<p>"


		cursor = connection.cursor()
		query = '''SELECT TABLES.TABLE_NAME as tablename, pg_description.description as table_descripcion FROM
					information_schema.TABLES
					LEFT JOIN pg_class ON TABLES.TABLE_NAME::name = pg_class.relname
					LEFT JOIN pg_description ON pg_class.oid = pg_description.objoid AND pg_description.objsubid = 0
					WHERE TABLES.table_schema::text = %s::text AND TABLES.table_type = 'BASE TABLE'::text ORDER BY
                    TABLES.TABLE_NAME ASC'''
		cursor.execute(query, [SCHEMA])
		columns = [x.name for x in cursor.description]
		tablas = cursor.fetchall()



		for tabla in tablas:
			row = dict(zip(columns, tabla))
			#print 'TABLA: '+row['tablename']
			#print 'DESCRIPCION: ' + '' if row['table_descripcion'] is None else 'DESCRIPCION: ' + row['table_descripcion']

			sourceHTML += "<table border = 1 width = '100%' cellpadding = '4' cellspacing = '0'>"
			sourceHTML += "<tr>"
			sourceHTML += "<td style = 'width:15%;'><b>TABLA:</b></td>"
			sourceHTML += "<td>%s</td>" % (row['tablename'])
			sourceHTML += "</tr>"
			sourceHTML += "<tr>"
			sourceHTML += "<td style = 'width: 15%;'><b>DESCRIPCIÓN:</b></td>"
			sourceHTML += "<td>%s</td>" % ('' if row['table_descripcion'] is None else row['table_descripcion'])
			sourceHTML += "</tr>"
			sourceHTML += "</table>"


			cursora = connection.cursor()
			querya = '''SELECT COLUMNS.column_name, COLUMNS.data_type, COLUMNS.column_default, COLUMNS.is_nullable,
                    COLUMNS.character_maximum_length, pg_description.description FROM information_schema.COLUMNS
                    LEFT JOIN pg_class ON COLUMNS.TABLE_NAME::name = pg_class.relname LEFT JOIN
                    pg_description ON pg_class.oid = pg_description.objoid AND
                    COLUMNS.ordinal_position::INTEGER = pg_description.objsubid
                    WHERE COLUMNS.table_schema::text = 'general'::text AND COLUMNS.TABLE_NAME = %s
					ORDER BY COLUMNS.TABLE_NAME ASC, COLUMNS.ordinal_position ASC'''

			cursora.execute(querya, [row['tablename']])
			columnsss = [z.name for z in cursora.description]
			columnas = cursora.fetchall()

			sourceHTML += "<table width='100%' border = 1 cellpadding = '4' cellspacing = '0'>"
			sourceHTML += "<tr>"
			sourceHTML += "<td width='32%'><b>NOMBRE</b></td>"
			sourceHTML += "<td width='34%'><b>TIPO</b></td>"
			sourceHTML += "<td width='17%'><b>LONGITUD</b></td>"
			sourceHTML += "<td width='10%'><b>NULO</b></td>"
			sourceHTML += "<td><b>DESCRIPCIÓN</b></td>"
			sourceHTML += "</tr>"

			for columna in columnas:
				row = dict(zip(columnsss, columna))

				sourceHTML += "<tr>"
				sourceHTML += "<td>%s</td>" % (row['column_name'])
				sourceHTML += "<td>%s</td>" % (row['data_type'])
				sourceHTML += "<td align='center'>%s</td>" % ('--' if row['character_maximum_length'] is None else row['character_maximum_length'])
				sourceHTML += "<td align='center'>%s</td>" % (row['is_nullable'])
				sourceHTML += "<td>%s</td>" % ('--' if row['description'] is None else row['description'])
				sourceHTML += "</tr>"

			sourceHTML += "</table><br><br>"

		sourceHTML += "</p></body></html>"

		outFilename = "Diccionario_BDAI.pdf"
		outFile = open(outFilename, "w+b")
		pisaStatus = pisa.CreatePDF(sourceHTML, dest=outFile)
		outFile.close()
		print "Termino"