# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def index(request):
	return render(request, 'dashboard/index.html', {})


@login_required
def mapainteractivo(request):
	return render(request, 'dashboard/mapainteractivo.html', {})

@login_required
def getgeojson(request):
	return render(request, 'dashboard/point.geo.json', {})