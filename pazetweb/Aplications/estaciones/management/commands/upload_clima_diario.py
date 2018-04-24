# -*- coding: utf-8 -*-
# Import needed libs
from datetime import datetime
from django.core.management.base import BaseCommand
import csv, codecs
from django.core.exceptions import ObjectDoesNotExist
from os import listdir
import os, sys
from Aplications.estaciones.models import EstnEstacion
from Aplications.clima.models import ClimaDiario
import time
import logging

reload(sys)
sys.setdefaultencoding('utf8')

#from threading import Thread
#def postpone(function):
#  def decorator(*args, **kwargs):
#    t = Thread(target = function, args=args, kwargs=kwargs)
#    t.daemon = True
#    t.start()
#  return decorator

# Start definition of custom command

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Comando para cargar csv de clima diario'

    def add_arguments(self, parser):
        parser.add_argument('ruta', type=str)
        #parser.add_argument('log', type=str)

    #@classmethod
    def handle(self, *args, **options):
        print options['ruta']
        #print options['log']
        #quit()
        # Define the paths for each variable
        rutasPosibles = {#'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo1/DATOS',
                #11'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo2/DATOS',
                #10'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo1/DATOS',
                #9'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo2/DATOS',
                #8'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo1/DATOS',
                #7'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo2/DATOS',
                #6'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo1/DATOS',
                #5'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo2/DATOS',
                #4'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo1/DATOS',
                #3'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo2/DATOS',
                #2'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo1/DATOS',
                #1'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo2/DATOS'

                'brillo1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo1/DATOS',
                'brillo2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo2/DATOS',
                'hum1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo1/DATOS',
                'hum2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo2/DATOS',
                'ppt1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo1/DATOS',
                'ppt2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo2/DATOS',
                'tmax1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo1/DATOS',
                'tmax2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo2/DATOS',
                'tmed1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo1/DATOS',
                'tmed2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo2/DATOS',
                'tmin1':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo1/DATOS',
                'tmin2':'/Users/Diego/Documents/Clientes/Corpoica/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo2/DATOS'
        };

        #listdir(rutaVariable)

        #quit()

        logging.basicConfig(filename=options['ruta']+'.log', level=logging.DEBUG)

        existPath = rutasPosibles.get(options['ruta'], -1)

        if existPath != -1:

            ruta = [existPath]
            #quit()

            # Definición de variables para obtener el campo a editar dependiendo del nombre de la carpeta que lo contenga
            variables = {
                "brillo": "cdia_brillo_solar",
                "hum": "cdia_humedad_relativa",
                "ppt": "cdia_precipitacion",
                "tmax": "cdia_temp_maxima",
                "tmed": "cdia_temp_media",
                "tmin": "cdia_temp_minima"
            }
            # Inicializamos contadores para llevar registro de datos creados, actualizados y fallidos
            createdCounter = 0
            wrongValueCounter = 0
            updatedCounter = 0
            notUpdatedCounter = 0
            noneExistingEstation = 0
            totalCount = 0

            # Inicia iteración de rutas
            for rutaVariable in ruta:

                # Obtiene dinámicamente el grupo con base en el nombre de la carpeta padre (1 o 2)
                grupo = rutaVariable.split('/')[-2][-1]

                # Obtengo nombre de variable en la carpeta de la ruta actual
                update_variable = rutaVariable.split('/')[-3]
                update_variable = variables.get(update_variable, -1)

                # Si nuestra carpeta está en la lista de variables obtendremos el campo que vamos a actualizar según la carpeta en la que estemos
                if  update_variable != -1:
                    # Obtenemos todos los archivos de la ruta actual y los iteramos
                    for nombreArchivo in listdir(rutaVariable):
                        # Creamos array con base en el guión bajo, así obtendremos en la posición cero del array resultante el código de la estación
                        estacionNumber = nombreArchivo.split("_")
                        estacionNumber = estacionNumber[0]
                        print estacionNumber
                        # Obtengo el objeto estación para ponerlo en la edición
                        try:
                            estacion = EstnEstacion.objects.get(estn_codigo=estacionNumber)


                            # Leemos el archivo
                            reader = csv.DictReader(codecs.open(rutaVariable + '/' + nombreArchivo, 'rU', encoding='ISO-8859-1'), delimiter=",")
                            # Iniciamos lectura línea a línea del archivo actual iterando todas las líneas del archivo
                            for line in reader:
                                # Iniciamos cuenta total de registros procesados
                                totalCount += 1
                                # Inicializo variable que almacenará el campo a editar o crear en la tabla
                                update_value = ""
                                # Por regla de negocio, se intentará obtener primero el valor qc 2, que es el más actualizado, sino existe continuará con el qc y sino lo tiene usará el valor
                                if  'VALOR_QC_2' in line:
                                    update_value = line.pop('VALOR_QC_2').replace(',', '.')
                                else:
                                    if 'VALOR_QC' in line:
                                        update_value = line.pop('VALOR_QC').replace(',', '.')
                                    else:
                                        update_value = line.pop('VALOR').replace(',', '.')

                                # Obtenemos la fecha de la línea actual requericdos para crear o actualizar
                                req_fecha = line.pop('fechas_datos')
                                # Obtengo la fecha en el formato requerido
                                fecha = datetime.strptime(req_fecha, '%Y-%m-%d').date()
                                # Se purifica el proceso evitando mediciones erradas que son las que tienen el valor 99999
                                if update_value != '99999' :
                                    # Uso un try catch para el caso en que no exista el registro para la presente estación en la fecha de la iteración actual
                                    try:
                                        currentClima = ClimaDiario.objects.get(estn=estacionNumber, cdia_fecha_reporte=fecha)
                                        # Obtengo el valor de la variable dinámica que necesitamos de clima
                                        currentVariableValue = str(getattr(currentClima, update_variable))
                                        # Si el valor actual en la base de datos es igual al que se va a actualizar entonces no procesa el registro y guarda el log
                                        if float(currentVariableValue) == float(update_value):
                                            notUpdatedCounter += 1
                                            self.stdout.write(self.style.ERROR('SAME VALUE: {}) {} - {} - {} - {} - {}'.format(notUpdatedCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                                            logging.info(self.style.ERROR('SAME VALUE: {}) {} - {} - {} - {} - {}'.format(notUpdatedCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                                        else:
                                            updatedCounter += 1
                                            self.stdout.write(self.style.SUCCESS('UPDATED: {}) {} - {} - {} - Old Value {} - New Value {} - {}'.format(updatedCounter, estacionNumber, fecha, update_variable, currentVariableValue, update_value, grupo)))
                                            logging.info(self.style.SUCCESS('UPDATED: {}) {} - {} - {} - Old Value {} - New Value {} - {}'.format(updatedCounter, estacionNumber, fecha, update_variable, currentVariableValue, update_value, grupo)))
                                            climaDiario = ClimaDiario.objects.update_or_create(estn=estacion, cdia_fecha_reporte=fecha, defaults={update_variable: update_value, 'cdia_calidad': grupo})
                                    except ObjectDoesNotExist:
                                        currentClima = ""
                                        createdCounter += 1
                                        self.stdout.write(self.style.SUCCESS('CREATED {}) {} - {} - {} - {} - {}'.format(createdCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                                        logging.info(self.style.SUCCESS('CREATED {}) {} - {} - {} - {} - {}'.format(createdCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                                        climaDiario = ClimaDiario.objects.update_or_create(estn=estacion, cdia_fecha_reporte=fecha, defaults={update_variable: update_value, 'cdia_calidad':grupo})
                                    #quit()
                                else:
                                    wrongValueCounter += 1
                                    #self.stdout.write(self.style.ERROR('{}) {} - {} - {} - {} - {}'.format(notSavedCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                                    #logging.warning(self.style.ERROR('{}) {} - {} - {} - {} - {}'.format(notSavedCounter, estacionNumber, fecha, update_variable, update_value, grupo)))
                        except ObjectDoesNotExist:
                            noneExistingEstation += 1
                            self.stdout.write(self.style.ERROR('NON EXISTING ESTATION: {}) {} - {} - {}'.format(noneExistingEstation, estacionNumber, update_variable, grupo)))
                            logging.info(self.style.ERROR('NON EXISTING ESTATION: {}) {} - {} - {}'.format(noneExistingEstation, estacionNumber, update_variable, grupo)))
            # Created some reports about saved, updated and
            self.stdout.write(self.style.SUCCESS('<<<----------------------------------------- FINALIZA DE LEER LOS DOCUMENTOS ----------------------------------------->>>'))
            self.stdout.write(self.style.SUCCESS('<<<----------------------------------------- FINAL REPORT: CREATED RECORDS -> {} - UPDATED RECORDS {} - WRONG MEASURES (99999) {} - TOTAL {} ----------------------------------------->>>'.format(createdCounter, updatedCounter, wrongValueCounter, totalCount)))
            logging.info('<<<----------------------------------------- FINAL REPORT: CREATED RECORDS -> {} - UPDATED RECORDS {} - WRONG MEASURES (99999) {} - TOTAL {} ----------------------------------------->>>'.format(createdCounter, updatedCounter, wrongValueCounter, totalCount))
            ahora = time.strftime("%c")
            self.stdout.write(self.style.SUCCESS('<<<----------------------------------------- FIN (%s) ----------------------------------------->>>' % ahora))
        else:
            print "Unknown path "+options['ruta']
