# -*- coding: utf-8 -*-
from django.conf.urls import url
from .import views



#BASE = 'agua/'

urlpatterns = [

url(r'index$', views.index, name='index'),

url(r'caudal_day$', views.caudal_day, name='caudal_day'),


url(r'caudal_day_download_csv$', views.caudal_day_download_csv, name='caudal_day_download_csv'),

# ---------------------------------------------------------------------------------------
# ------------------------------------ JSON ---------------------------------------------
# ---------------------------------------------------------------------------------------

# CAUDALES DIARIOS DE UNA ESTACION EN UN AÑO
url(r'caudal_day_estn_year_json$', views.caudal_day_estn_year_json, name='caudal_day_estn_year_json'),


# CURVA DE DURACIÓN DE CAUDAL DE UNA ESTACION
url(r'cdc_diaria_estn_json$', views.cdc_diaria_estn_json, name='cdc_diaria_estn_json'),


# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------
#url(r'all_stations_geojson$', views.all_stations_geojson, name='all_stations_geojson'),

]