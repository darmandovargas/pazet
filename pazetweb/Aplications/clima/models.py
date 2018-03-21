# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.estaciones.models import EstnEstacion
from django.db import models

# Create your models here.
class ClimaEscenariosCc(models.Model):
    escc_id = models.BigAutoField(primary_key=True)
    escc_nombre = models.CharField("Escenario", unique=True, max_length=50)
    escc_created = models.DateTimeField("Registro", auto_now_add=True)
    escc_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.escc_nombre)

    class Meta:
        managed = True
        db_table = 'clima_escenarios_cc'
        #db_table = u'general"."clima_escenarios_cc'
        verbose_name = 'Escenario cambio climatico'
        verbose_name_plural = 'Escenarios cambio climatico'


class ClimaCo2(models.Model):
    cotwo_id = models.BigAutoField(primary_key=True)
    escc = models.ForeignKey(ClimaEscenariosCc, verbose_name="Escenarios CC")
    cotwo_year = models.SmallIntegerField("Año")
    cotwo_contenido = models.FloatField("Contenido de CO2")
    cotwo_created = models.DateTimeField("Registro", auto_now_add=True)
    cotwo_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.escc)

    class Meta:
        managed = True
        db_table = 'clima_co2'
        verbose_name = 'CO2'
        verbose_name_plural = 'CO2s'


class ClimaDiario(models.Model):
    cdia_id = models.BigAutoField(primary_key=True)
    estn = models.ForeignKey(EstnEstacion, db_column='estn_codigo', verbose_name="Estación")
    cdia_fecha_reporte = models.DateField("Fecha reporte")
    cdia_precipitacion = models.FloatField("Precipitación", blank=True, null=True)
    cdia_temp_media = models.FloatField("Temperatura Media", blank=True, null=True)
    cdia_temp_minima = models.FloatField("Temperatura Minima", blank=True, null=True)
    cdia_temp_maxima = models.FloatField("Temperatura Maxima", blank=True, null=True)
    cdia_humedad_relativa = models.FloatField("Humedad relativa", blank=True, null=True)
    cdia_brillo_solar = models.FloatField("Brillo solar", blank=True, null=True)
    cdia_evaporacion = models.FloatField("Evaporación", blank=True, null=True)
    cdia_vel_viento = models.FloatField("Velocidad viento", blank=True, null=True)
    cdia_calidad = models.SmallIntegerField("Calidad", blank=True, null=True)
    cdia_created = models.DateTimeField("Registro", auto_now_add=True)
    cdia_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.estn)

    class Meta:
        managed = False
        db_table = 'clima_diario'
        unique_together = (('estn', 'cdia_fecha_reporte'),)
        verbose_name = 'Clima diario'
        verbose_name_plural = 'Clima diario'


class ClimaMensual(models.Model):
    cmen_id = models.BigAutoField(primary_key=True)
    estn = models.ForeignKey(EstnEstacion, db_column='estn_codigo', verbose_name="Estación")
    cmen_year = models.SmallIntegerField("Año")
    cmen_month = models.SmallIntegerField("Mes")
    cmen_precipitacion = models.FloatField("Precipitación", blank=True, null=True)
    cmen_temp_media = models.FloatField("Temperatura media", blank=True, null=True)
    cmen_temp_min = models.FloatField("Temperatura minima", blank=True, null=True)
    cmen_temp_max = models.FloatField("Temperatura maxima", blank=True, null=True)
    cmen_humedad_relativa = models.FloatField("Humedad relativa", blank=True, null=True)
    cmen_brillo_solar = models.FloatField("Brillo solar", blank=True, null=True)
    cmen_vel_viento = models.FloatField("Velocidad viento", blank=True, null=True)
    cmen_evaporacion = models.FloatField("Evaporación", blank=True, null=True)
    cmen_created = models.DateTimeField("Registro", auto_now_add=True)
    cmen_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.estn)

    class Meta:
        managed = False
        db_table = 'clima_mensual'
        unique_together = (('estn', 'cmen_year', 'cmen_month'),)
        verbose_name = 'Clima mensual'