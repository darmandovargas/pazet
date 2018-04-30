# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from qgis.core import *
from getpass import getuser



class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Comando para cargar csv de muestras tomadas en azosulia'

    def handle(self, *args, **options):

        # ---------------------------------------------------------------------------------------
        #QgsApplication.setPrefixPath("/usr/share/qgis", True)
        QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS", True)
        qgs = QgsApplication([], True)
        qgs.initQgis()
        #---------------------------------------------------------------------------------------

        # CONSULTA POSTGIS
        sql = '''(select pfis.pfis_id, mues.mues_coordenadas, pfis.pfis_densidad_real 
        from general.suelo_muestra as mues inner join general.suelo_propfisica as pfis 
        on (pfis.mues_id=mues.mues_id) 
        where mues.mues_id like '%ZULIA%' and pfis.pfis_densidad_real is not null)'''

        uri = QgsDataSourceURI()
        # Nombre del servidor, puerto, nombre de la base de datos, usuario y contraseña
        uri.setConnection("localhost", "5432", "bdpazet", "administrador", "postgres")
        # Consulta, columna con geometria, columna con identificador
        uri.setDataSource("", sql, "mues_coordenadas", "", "pfis_id")
        pointLayer = QgsVectorLayer(uri.uri(), "muestras", "postgres")

        #sys.path.append('/usr/share/qgis/python/plugins')
        from processing.core.Processing import Processing
        Processing.initialize()
        from processing.tools import *


        path = '/home/shamirtv/Documentos/voronoi.shp'
        if pointLayer.isValid():
            #print Processing.getAlgorithm("qgis:voronoipolygons")
            general.runalg("qgis:voronoipolygons", pointLayer, 0, path)
            #QgsVectorFileWriter.writeAsVectorFormat(pointLayer, path, "utf-8", None, "ESRI Shapefile")





        #writer = QgsVectorFileWriter.writeAsVectorFormat(pointLayer, path, "utf-8", None, "ESRI Shapefile", True)


        # ---------------------------------------------------------------------------------------
        qgs.exitQgis()
        # ---------------------------------------------------------------------------------------

        self.stdout.write(self.style.SUCCESS('Termino'))
