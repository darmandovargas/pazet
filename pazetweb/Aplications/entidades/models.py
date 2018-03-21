# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class EntdsEntidad(models.Model):
    entds_id = models.SmallIntegerField(primary_key=True)
    entds_nombre = models.CharField("Nombre entidad", unique=True, max_length=200)
    entds_siglas = models.CharField("Siglas", unique=True, max_length=10)
    entds_created = models.DateTimeField("Registro", auto_now_add=True)
    entds_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.entds_nombre)

    class Meta:
        managed = False
        db_table = 'entds_entidad'
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'