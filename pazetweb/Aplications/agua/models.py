# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.estaciones.models import EstnEstacion
from django.db import models

# Create your models here.
class CaudalDiario(models.Model):
    caudi_id = models.BigAutoField(primary_key=True)
    estn = models.ForeignKey(EstnEstacion, db_column='estn_codigo', verbose_name="Estacion")
    caudi_fecha_reporte = models.DateField("Fecha reporte")
    caudi_caudal = models.FloatField("Caudal")
    caudi_created = models.DateTimeField("Registro", auto_now_add=True)
    caudi_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.estn)

    class Meta:
        managed = False
        db_table = 'caudal_diario'
        unique_together = (('caudi_fecha_reporte', 'estn'),)
        verbose_name = 'Caudal diario'
        verbose_name_plural = 'Caudales diarios'