# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models as Geomodels
from Aplications.orgtecol.models import Municipio
from django.db import models

# Create your models here.
class Cultivo(models.Model):
    cul_id = models.BigAutoField(primary_key=True)
    cul_nombre = models.CharField("Tipo de Cultivo", unique=True, max_length=50)
    cul_created = models.DateTimeField("Registro", auto_now_add=True)
    cul_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.cul_nombre)


    class Meta:
        managed = True
        db_table = 'cultivo'
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'


class TipoCultivo(models.Model):
    tipcul_id = models.BigAutoField(primary_key=True)
    cul_id = models.ForeignKey(Cultivo, verbose_name="Cultivo")
    tipcul_nombre = models.CharField("Nombre de Cultivo", unique=True, max_length=50)
    tipcul_created = models.DateTimeField("Registro", auto_now_add=True)
    tipcul_updated = models.DateTimeField("Actualización", auto_now=True)


    def __unicode__(self):
        return '{}'.format(self.tipcul_nombre)


    class Meta:
        managed = True
        db_table = 'cul_tipo_cultivo'
        verbose_name = 'Tipo de Cultivo'
        verbose_name_plural = 'Tipos de Cultivos'

class NivelFreatico(models.Model):
    nivfre_id = models.BigAutoField(primary_key=True)
    nivfre_nombre = models.CharField("Tipo de Cultivo", unique=True, max_length=50)
    nivfre_coordenadas = Geomodels.PointField("Coordenadas Nivel Freático", srid=4326, help_text="Seleccione un punto de ubicación")
    nivfre_altitud = models.IntegerField("Altitud")
    mun_id = models.ForeignKey(Municipio, verbose_name="Municipio")
    nivfre_created = models.DateTimeField("Registro", auto_now_add=True)
    nivfre_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.nivfre_nombre)


    class Meta:
        managed = True
        db_table = 'cul_nivel_freatico'
        verbose_name = 'Nivel Freático'
        verbose_name_plural = 'Niveles Freáticos'


