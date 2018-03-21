# -*- coding: utf-8 -*-

from qgis.core import *
from PyQt4.QtCore import QVariant

class LayerCreate():

    def __init__(self):
        pass

    def LayerPoint(self, listpoint, data = []):

        # ---------------------------------------------------------------------------------------
        #QgsApplication.setPrefixPath("/usr/share/qgis", True)
        #qgs = QgsApplication([], True)
        #qgs.initQgis()
        # ---------------------------------------------------------------------------------------

        poinlayer = QgsVectorLayer("Point?crs=epsg:4326", "temporary_points", "memory")
        pr = poinlayer.dataProvider()

        n = len(listpoint)

        # add fields
        if len(data)<=0 or len(data)!=len(listpoint):
            pr.addAttributes([ QgsField("id", QVariant.Int) ])
        else:
            pr.addAttributes([QgsField("id", QVariant.Int), QgsField("data", QVariant.Int)])
        poinlayer.updateFields()  # tell the vector layer to fetch changes from the provider

        for index, point in enumerate(listpoint):
            # add a feature
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(point[0], point[1])))
            if len(data) <= 0 or len(data) != len(listpoint):
                fet.setAttributes([index])
            else:
                fet.setAttributes([index, data[index] ])
            pr.addFeatures([fet])

        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        poinlayer.updateExtents()

        #path = '/home/shamirtv/Documentos/puntos.shp'
        #QgsVectorFileWriter.writeAsVectorFormat(vl, path, "utf-8", None,"ESRI Shapefile")

        # ---------------------------------------------------------------------------------------
        #qgs.exitQgis()
        # ---------------------------------------------------------------------------------------

        return poinlayer