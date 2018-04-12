# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.management.base import BaseCommand
import csv, codecs
#from clima.models import Estaciones, BaseMensual
from os import listdir
from Aplications.estacion.models import EstnEstacion
from Aplications.clima.models import ClimaDiario
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Comando para cargar csv de clima diario'

    def handle(self, *args, **options):

        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo1/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/brillo/Grupo2/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo1/DATOS'
        #ruta =  '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/hum/Grupo2/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo1/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/ppt/Grupo2/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo1/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmax/Grupo2/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo1/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmed/Grupo2/DATOS'
        #ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo1/DATOS'
        ruta = '/home/storres/Documentos/CORPOICA/Datos_diarios_Base_IDEAM_Jul_20162017/entrega final/DATOS_FINAL/tmin/Grupo2/DATOS'

        # ------------------------------------ CONFIGURACIONES DE ARRANQUE ---------------------

        grupo = 2
        update_variable = 'cdia_temp_minima'
        file_var= 'VALOR_QC_2'
        cont = 0

        # -------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------

        listcod = ['16010010','16010020','16010040','16010050','16010060','16010070','16010080','16010090','16010100',
                    '16010110','16010150','16010170','16010190','16010290','16010330','16010340','16015010','16015020',
                   '16015030','16015040','16015050','16015080','16015090','16015100','16015110','16015120','16015130',
                   '16015140','16015501','16020010','16020030','16020050','16020060','16020080','16020090','16020110',
                   '16020120','16020130','16020140','16020150','16020160','16020170','16020180','16020190','16020200',
                   '16020210','16020220','16020230','16020240','16020250','16020260','16020270','16020280','16020290',
                   '16020300','16020310','16020320','16020340','16020350','16020360','16020370','16020390','16020510',
                   '16020520','16025010','16025020','16025030','16025040','16025050','16025070','16025080','16030030',
                   '16030040','16030050','16030060','16030080','16030120','16030130','16030140','16030150','16035010',
                   '16035020','16035030','16035040','16035050','16060010','16070010','16070020','16070030','16070040',
                   '37010070','37010080','37015010']

        for cosa in listdir(ruta):
            if cosa[:-9] in listcod:

                cont += 1 # CONTADOR PARA MONITOREAR EL PROCESO

                estacion = EstnEstacion.objects.get(estn_codigo=cosa[:-9])

                reader = csv.DictReader(codecs.open(ruta+'/'+cosa, 'rU', encoding='ISO-8859-1'), delimiter=",")
                index = 0
                for line in reader:
                    req_fecha = line.pop('fechas_datos')
                    req_valor = line.pop(file_var).replace(',', '.')


                    fecha = datetime.strptime(req_fecha, '%Y-%m-%d').date()

                    if req_valor != '99999':
                        clima, created = ClimaDiario.objects.update_or_create(
                            cdia_fecha_reporte=fecha, estn=estacion, defaults={update_variable: req_valor, 'cdia_calidad':grupo}
                        )
                        self.stdout.write(self.style.SUCCESS('{}) {} - {} - {}'.format(cont, estacion, fecha, req_valor)))
                    else:
                        self.stdout.write(self.style.ERROR('{} - {} - {}'.format(estacion, fecha, req_valor)))


                self.stdout.write(self.style.SUCCESS('Termino documento -----------------------------------------<<<'))

        ahora = time.strftime("%c")
        self.stdout.write(self.style.SUCCESS('Termino Directorio ----------------------------------------->> FIN SCRIPT (%s)' % ahora))