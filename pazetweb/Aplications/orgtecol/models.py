# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models as Geomodels
from django.db import models

# Create your models here.
class Region(models.Model):
    reg_id = models.AutoField(primary_key=True)
    reg_nombre = models.CharField("Región", unique=True, max_length=100)
    reg_delimitacion = Geomodels.MultiPolygonField(blank=True, null=True)
    reg_created = models.DateTimeField("Registro", auto_now_add=True)
    reg_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return str(self.reg_nombre)

    class Meta:
        managed = True
        db_table = 'orgtecol_region'
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


class Departamento(models.Model):
    depto_codigodane = models.CharField("Codigo dane", max_length=10, primary_key=True)
    reg = models.ForeignKey(Region, verbose_name='Región')
    depto_nombre = models.CharField("Nombre", max_length=100)
    depto_iso = models.CharField("ISO", max_length=10)
    depto_delimitacion = Geomodels.MultiPolygonField("Delimitación", help_text="Delimitación geografica", blank=True, null=True)
    depto_created = models.DateTimeField("Registro", auto_now_add=True)
    depto_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return str(self.depto_nombre)

    class Meta:
        managed = True
        db_table = 'orgtecol_departamento'
        unique_together = (('reg', 'depto_nombre'),)
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Municipio(models.Model):
    mun_id = models.AutoField(primary_key=True)
    depto = models.ForeignKey(Departamento, verbose_name='Departamento', db_column='depto_codigodane')
    mun_nombre = models.CharField("Nombre", max_length=100)
    mun_codigodane = models.CharField("Codigo Dane", unique=True, max_length=10, blank=True, null=True)
    mun_delimitacion = Geomodels.MultiPolygonField("Delimitación", help_text="Delimitación geografica", blank=True, null=True)
    mun_created = models.DateTimeField("Registro", auto_now_add=True)
    mun_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return str(self.mun_nombre)

    class Meta:
        managed = True
        ordering = ('mun_nombre',)
        db_table = 'orgtecol_municipio'
        unique_together = (('depto', 'mun_nombre'),)
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'