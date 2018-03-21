# -*- coding: utf-8 -*-
from django.conf import settings
from qgis.core import *

class Thiessen():

    def __init__(self):
        pass


    def voronoi(self):

        # ---------------------------------------------------------------------------------------
        #QgsApplication.setPrefixPath("/usr/share/qgis", True)
        #qgs = QgsApplication([], True)
        #qgs.initQgis()
        # ---------------------------------------------------------------------------------------

        import processing
        from processing.core.Processing import Processing
        #try:
        Processing.initialize()

        path = '/home/shamirtv/Documentos/puntos.shp'

        layer = QgsVectorLayer(path, "testlayer_shp", "ogr")

        if not layer.isValid():
            print "fallo la carga del layer!"
        else:
            print "Layer cargado correctamente!"

        #except ValueError:
        #    print ValueError

        # ---------------------------------------------------------------------------------------
        #qgs.exitQgis()
        # ---------------------------------------------------------------------------------------