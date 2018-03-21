from django.conf.urls import url
from .import views



#BASE = 'estaciones/'

urlpatterns = [


# ---------------------------------------------------------------------------------------
# ------------------------------------ JSON ---------------------------------------------
# ---------------------------------------------------------------------------------------
url(r'estacion_get_with_codigo$', views.estacion_get_with_codigo, name='estacion_get_with_codigo'),


url(r'data_history/(?P<codigo>\w+)?$', views.data_history, name='data_history'),


# CLIMA MENSUAL
url(r'filtro_estn_in_poligon_cmonth_json$', views.filtro_estn_in_poligon_cmonth_json, name='filtro_estn_in_poligon_cmonth_json'),
url(r'estn_clima_month_depto_json$', views.estn_clima_month_depto_json, name='estn_clima_month_depto_json'),
url(r'estn_clima_month_mun_json$', views.estn_clima_month_mun_json, name='estn_clima_month_mun_json'),
url(r'estn_codigo_clima_month_json$', views.estn_codigo_clima_month_json, name='estn_codigo_clima_month_json'),
url(r'estn_name_clima_month_json$', views.estn_name_clima_month_json, name='estn_name_clima_month_json'),



# CLIMA DIARIO
url(r'filtro_estn_in_poligon_cday_json$', views.filtro_estn_in_poligon_cday_json, name='filtro_estn_in_poligon_cday_json'),
url(r'estn_clima_day_depto_json$', views.estn_clima_day_depto_json, name='estn_clima_day_depto_json'),
url(r'estn_clima_day_mun_json$', views.estn_clima_day_mun_json, name='estn_clima_day_mun_json'),
url(r'estn_codigo_clima_day_json$', views.estn_codigo_clima_day_json, name='estn_codigo_clima_day_json'),
url(r'estn_name_clima_day_json$', views.estn_name_clima_day_json, name='estn_name_clima_day_json'),



# CAUDAL DIARIO
url(r'filtro_estn_in_poligon_cauday_json$', views.filtro_estn_in_poligon_cauday_json, name='filtro_estn_in_poligon_cauday_json'),
url(r'estn_caudal_day_depto_json$', views.estn_caudal_day_depto_json, name='estn_caudal_day_depto_json'),
url(r'estn_caudal_day_mun_json$', views.estn_caudal_day_mun_json, name='estn_caudal_day_mun_json'),
url(r'estn_codigo_caudal_day_json$', views.estn_codigo_caudal_day_json, name='estn_codigo_caudal_day_json'),
url(r'estn_name_caudal_day_json$', views.estn_name_caudal_day_json, name='estn_name_caudal_day_json'),





# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------
url(r'all_stations_geojson$', views.all_stations_geojson, name='all_stations_geojson'),

url(r'all_estn_clima_month_geojson$', views.all_estn_clima_month_geojson, name='all_estn_clima_month_geojson'),
url(r'all_estn_clima_day_geojson$', views.all_estn_clima_day_geojson, name='all_estn_clima_day_geojson'),
url(r'all_estn_caudal_diario_geojson$', views.all_estn_caudal_diario_geojson, name='all_estn_caudal_diario_geojson'),



]