# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Aplications.cultivo.models import Cultivo

# Create your views here.
@login_required
def index(request):
	return render(request, 'dashboard/cultivo/index.html', {})

@login_required
def herbaseos_frutas_granos(request):
	tipo="Herbáseos Frutas y Granos"
	cultivo=Cultivo.objects.filter(cul_tipo_cultivo='Herbáseos Frutas y Granos')
	print cultivo
	return render(request, 'dashboard/cultivo/tipo_cultivo.html',{'tipo':tipo,'cultivo':cultivo})

@login_required
def herbaseos_vegetales_hoja(request):
	tipo="Herbáseos Vegetales de Hoja"
	cultivo=Cultivo.objects.filter(cul_tipo_cultivo='Herbáseos Vegetales de Hoja')	
	return render(request, 'dashboard/cultivo/tipo_cultivo.html',{'tipo':tipo,'cultivo':cultivo})

@login_required
def herbaseos_raices_tuberculos(request):
	tipo="Herbáseos Raices y Tuberculos"
	cultivo=Cultivo.objects.filter(cul_tipo_cultivo='Herbáseos Raices y Tuberculos')	
	return render(request, 'dashboard/cultivo/tipo_cultivo.html',{'tipo':tipo,'cultivo':cultivo})

@login_required
def herbaseos_cultivos_forrajeros(request):
	tipo="Herbáseos Cultivos Forrajeros"
	cultivo=Cultivo.objects.filter(cul_tipo_cultivo='Herbáseos Cultivos Forrajeros')	
	return render(request, 'dashboard/cultivo/tipo_cultivo.html',{'tipo':tipo,'cultivo':cultivo})

@login_required
def arboreos(request):
	tipo="Arbóreos"
	cultivo=Cultivo.objects.filter(cul_tipo_cultivo='Arbóreos')	
	return render(request, 'dashboard/cultivo/tipo_cultivo.html',{'tipo':tipo,'cultivo':cultivo})



