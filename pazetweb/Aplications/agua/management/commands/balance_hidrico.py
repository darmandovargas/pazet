# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from Aplications.agua.library.caudales import Caudales
from Aplications.agua.models import CaudalDiario
from threading import Thread
import pandas as pd

class Command(BaseCommand):
    args = 'No necesita argumentos'
    help = 'Comando para calcular el balance hidrico de las estaciones hidrologicas'

    def handle(self, *args, **options):
        listCauEstReg = []

        def regionalizacion(codigo):
            caudales = Caudales()
            listCaudales, listProb, _, adf = caudales.curva_duracion_caudal_convencional(codigo)
            listCauEst = caudales.estandarizacion_por_adf(listCaudales, adf)
            listCauEstReg.extend(listCauEst)

        estaciones = CaudalDiario.objects.values('estn').distinct()
        for estacion in estaciones:
            subproceso = Thread(target=regionalizacion, args=(estacion['estn'],))
            subproceso.start()

        subproceso.join()

        listCauEstReg.sort(reverse=True) # SE ORDENA LA LISTA DE PROBABILIDADES DE MAYOR A MENOR

        df = pd.DataFrame(listCauEstReg, columns=['cauEstandReg'])
        df['enum'] = df.index.values + 1 # ENUMERACIÓN
        df['probReg'] = df['enum'] / ( len(df) + 1 ) # CALCULO DE LA PROBABILIDAD ESCALA REGIONAL


        print df