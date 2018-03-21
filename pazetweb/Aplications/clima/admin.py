# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Aplications.clima.models import ClimaEscenariosCc
from django.contrib import admin

# Register your models here.
@admin.register(ClimaEscenariosCc)
class EstnTipoAdmin(admin.ModelAdmin):
    list_display = ['__unicode__'] + [f.name for f in ClimaEscenariosCc._meta.fields]
