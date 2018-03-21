# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.orgtecol.models import Municipio
from Aplications.entidades.models import EntdsEntidad
from django.contrib.gis.db import models as Geomodels
from django.db import models

# Create your models here.
class EstnCategoria(models.Model):
    cat_id = models.AutoField("Id", primary_key=True)
    cat_nombre = models.CharField("Categoria", unique=True, max_length=50)
    cat_siglas = models.CharField("Siglas", unique=True, max_length=50)
    cat_created = models.DateTimeField("Registro", auto_now_add=True)
    cat_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.cat_nombre)

    class Meta:
        managed = False
        db_table = 'estn_categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class EstnClase(models.Model):
    clase_id = models.AutoField("Id", primary_key=True)
    clase_nombre = models.CharField("Clase", unique=True, max_length=50)
    clase_siglas = models.CharField("Siglas", unique=True, max_length=50)
    clase_created = models.DateTimeField("Registro", auto_now_add=True)
    clase_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.clase_nombre)

    class Meta:
        managed = False
        db_table = 'estn_clase'
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'


class EstnTipo(models.Model):
    tipo_id = models.AutoField("Id", primary_key=True)
    tipo_nombre = models.CharField("Tipo", unique=True, max_length=1000)
    tipo_siglas = models.CharField("Siglas", unique=True, max_length=100)
    tipo_created = models.DateTimeField("Registro", auto_now_add=True)
    tipo_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.tipo_nombre)

    class Meta:
        managed = False
        db_table = 'estn_tipo'
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'


class EstnEstacion(models.Model):

    ESTADOS = (
        ('ACT', 'ACTIVO'),
        ('SUS', 'SUSPENDIDO'),
    )
    estn_codigo = models.CharField("Codigo", max_length=50, primary_key=True)
    mun = models.ForeignKey(Municipio, verbose_name='Municipio')
    clase = models.ForeignKey(EstnClase, verbose_name='Clase')
    cat = models.ForeignKey(EstnCategoria, verbose_name='Categoria')
    tipo = models.ForeignKey(EstnTipo, verbose_name='Tipo')
    entds = models.ForeignKey(EntdsEntidad, verbose_name='Entidad')
    estn_nombre = models.CharField("Nombre", max_length=200)
    estn_corriente = models.CharField("Corriente", max_length=200, blank=True, null=True)
    estn_coordenadas = Geomodels.PointField("Coordenadas", srid=4326, help_text="Seleccione un punto de ubicación")
    estn_estado = models.CharField("Estado", choices=ESTADOS, max_length=10, blank=True,null=True,default=None)
    estn_altitud = models.FloatField("Altitud", blank=True, null=True)
    estn_fecha_instalacion = models.DateField("Fecha de instalación", blank=True, null=True)
    estn_fecha_suspension = models.DateField("Fecha de suspensión", blank=True, null=True)
    estn_created = models.DateTimeField("Registro", auto_now_add=True)
    estn_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.estn_codigo)

    @property
    def estn_lat(self):
        return float("{0:.3f}".format(self.estn_coordenadas.y))

    @property
    def estn_lng(self):
        return float("{0:.3f}".format(self.estn_coordenadas.x))

    class Meta:
        managed = False
        db_table = 'estn_estacion'
        verbose_name = 'Estación'
        verbose_name_plural = 'Estaciones'