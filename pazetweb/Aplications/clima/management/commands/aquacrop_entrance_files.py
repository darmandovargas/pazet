# -*- coding: utf-8 -*-
# Custom command to create Aquacrop plugin files for model entrance
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import connection

# Start definition of custom command
class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Comando para cargar csv de clima diario'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('station', type=str)
        parser.add_argument('periodo', type=str)
        parser.add_argument('initdate', type=str)
        parser.add_argument('enddate', type=str)

    def handle(self, *args, **options):

        filesInfo = {
            'tmp': ['Tmin (°C) TMax(°C)\n', 'temperature.TMP', 'Temperatura'],
            'eto': ['Promedio Eto (mm/día)\n', 'evapotranspiration.ETo', 'Evapotranspiración'],
            'plu': ['Precipitación Total (mm)\n', 'precipitation.PLU', 'Precipitación'],
            'co2': ['Año             CO2 (ppm por volumen)\n', 'media_anual_atmosferica.CO2', 'Media Anual Atmosféfica']
        };

        periodos = {
            'diario': 1,
            'decadal': 2,
            'mensual': 3
        };

        periodo = options['periodo']

        fileType = options['file'];
        fileHeader = filesInfo.get(options['file'], -1)[0]
        fileName = filesInfo.get(options['file'], -1)[1]
        variableName = filesInfo.get(options['file'], -1)[2]
        station = options['station']
        period = periodos.get(options['periodo'], 1)

        initdate = options['initdate'].split('-')
        initanio = initdate[0]
        initdia = initdate[1] #if tipo == "diario" else '01'
        initmes = initdate[2] #if tipo == "diario" or tipo == "mensual" else '01'

        enddate = options['enddate'].split('-')
        endanio = enddate[0]
        enddia = enddate[1] #if tipo == "diario" else '31'
        endmes = enddate[2] #if tipo == "diario" or tipo == "mensual" else '12'


        # if options['type'] == "diario":
        #     initdia = initdate[1]
        #     initmes = initdate[2]
        #     enddia = enddate[1]
        #     endmes = enddate[2]
        # elif options['type'] == "decadal":
        #     initdia = "01"
        #     initmes = "01"
        #     enddia = "31"
        #     endmes = "12"
        # elif options['type'] == "mensual":
        #     initdia = initdate[1]
        #     initmes = initdate[2]
        #     enddia = enddate[1]
        #     endmes = enddate[2]

        #else:


        if fileHeader != -1:
            #/Users/Diego/Documents/Clientes/Corpoica/pazet/pazetweb/aquacrop/
            with open('./aquacrop/'+fileName, 'w') as f:

                myfile = File(f)


                if fileType != "co2":
                    myfile.write('Archivo de entrada estación "' + station + '" para el modelo Aquacrop con datos de Clima (' + variableName + ')\n')
                    myfile.write( str(period) + ' : Registros diarios (1=diario, 2= decadal y 3=datos mensuales)\n')
                    myfile.write(initdia + ' : Primer día de registro (1, 11 o 21 para decadales o 1 para mensuales)\n')
                    myfile.write(initmes + ' : Primer mes del registro\n')
                    myfile.write(initanio + ' : Primer año del registro (1901 si no une a un año específico)\n')
                    myfile.write('\n')
                else:
                    myfile.write('Archivo de entrada para el modelo Aquacrop con datos de CO2 (' + variableName + ')\n')

                myfile.write(fileHeader)
                myfile.write('======================\n')

                if fileType != "co2":
                    if periodo != "mensual":
                        query = '''SELECT * FROM general.clima_diario WHERE estn_codigo='%s' AND 
                                    cdia_fecha_reporte >= '%s/%s/%s' AND 
                                    cdia_fecha_reporte <= '%s/%s/%s' 
                                    ORDER BY cdia_fecha_reporte
                                ''' % (station, initanio, initmes, initdia, endanio, endmes, enddia)
                    else:
                        query = '''SELECT * FROM general.clima_mensual WHERE estn_codigo = '%s' AND
                                    to_date(concat(cmen_year, cmen_month), 'YYYYMM') >= '%s/%s/01' AND
                                    to_date(concat(cmen_year, cmen_month), 'YYYYMM') <= '%s/%s/01' 
                                ''' % (station, initanio, initmes, endanio, endmes)
                else:
                    query = '''SELECT * FROM clima_co2 
                                WHERE cotwo_year >= '%s' AND cotwo_year <= '%s'
                                ORDER BY cotwo_year 
                            ''' % (initanio, endanio)

                print query

                cursor = connection.cursor()
                cursor.execute(query)
                columns = [x.name for x in cursor.description]
                climaList = cursor.fetchall()

                for clima in climaList:
                    row = dict(zip(columns, clima))
                    # Imprime en el archivo la variable dependiendo del tipo de archivo si es tmp, eto o plu para los casos diferentes al mensual
                    if fileType == "tmp" and periodo != "mensual" and row['cdia_temp_minima'] != None and row['cdia_temp_maxima'] != None:
                        myfile.write(str(row['cdia_temp_minima']) + '         ' + str(row['cdia_temp_maxima']) + '\n')
                    elif fileType == "eto" and periodo != "mensual" and row['cdia_evaporacion'] != None:
                        myfile.write(str(row['cdia_evaporacion']) + '\n')
                    elif fileType == "plu" and periodo != "mensual" and row['cdia_precipitacion'] != None:
                        myfile.write(str(row['cdia_precipitacion']) + '\n')
                    # Imprime en el archivo la variable dependiendo del tipo de archivo si es tmp, eto o plu para los casos de tipo mensual
                    elif fileType == "tmp" and periodo == "mensual" and row['cmen_temp_min'] != None and row['cmen_temp_max'] != None:
                        myfile.write(str(row['cmen_temp_min']) + '         ' + str(row['cmen_temp_max']) + '\n')
                    elif fileType == "eto" and periodo == "mensual" and row['cmen_evaporacion'] != None:
                        myfile.write(str(row['cmen_evaporacion']) + '\n')
                    elif fileType == "plu" and periodo == "mensual" and row['cmen_precipitacion'] != None:
                        myfile.write(str(row['cmen_precipitacion']) + '\n')

                    elif fileType == "co2" and row['cotwo_contenido'] != None:
                        myfile.write(str(row['cotwo_year']) + '        ' + str(row['cotwo_contenido']) + '\n')

                    else:
                        myfile.write('\n')

                myfile.closed
                f.closed
        else:
            self.stdout.write(self.style.ERROR('Please enter a valid file type in order to build the Aquacrop entrance file'))
