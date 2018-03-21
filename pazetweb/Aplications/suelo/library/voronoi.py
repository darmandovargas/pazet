# -*- coding: utf-8 -*-

from qgis.core import *

class Voronoi():

    def __init__(self):
        pass


    def poligonos(self, pointlayer):

        # ---------------------------------------------------------------------------------------
        QgsApplication.setPrefixPath("/usr/share/qgis", True)
        qgs = QgsApplication([], True)
        qgs.initQgis()
        # ---------------------------------------------------------------------------------------

        import processing
        from processing.core.Processing import Processing
        try:
            path = '/home/shamirtv/Documentos/voronoi.shp'
            Processing.initialize()

            processing.runalg("qgis:voronoipolygons", pointlayer, 0, path)
        except ValueError:
            print ValueError


        # ---------------------------------------------------------------------------------------
        QgsApplication.exitQgis()
        #---------------------------------------------------------------------------------------