from django.conf.urls import url
from .import views



#BASE = 'clima/'

urlpatterns = [

url(r'index$', views.index, name='index'),

url(r'clima_month$', views.clima_month, name='clima_month'), # RENDERIZACION DE TEMPLATES
url(r'clima_day$', views.clima_day, name='clima_day'), # RENDERIZACION DE TEMPLATES
url(r'dioxdc$', views.dioxdc, name='dioxdc'), # RENDERIZACION DE TEMPLATES


url(r'dioxdc_download/(?P<escenario_id>\w+)?', views.dioxdc_download, name='dioxdc_download'),
url(r'clima_month_download_csv$', views.clima_month_download_csv, name='clima_month_download_csv'),
url(r'clima_day_download_csv$', views.clima_day_download_csv, name='clima_day_download_csv'),


# ---------------------------------------------------------------------------------------
# ------------------------------------ JSON ---------------------------------------------
# ---------------------------------------------------------------------------------------

# (GRAFICA)
url(r'emisiones_with_escenario_json$', views.emisiones_with_escenario_json, name='emisiones_with_escenario_json'),

# (GRAFICA)
url(r'clima_month_estn_year_json$', views.clima_month_estn_year_json, name='clima_month_estn_year_json'),


url(r'clima_day_estn_year_json$', views.clima_day_estn_year_json, name='clima_day_estn_year_json'),





# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------
#url(r'all_stations_geojson$', views.all_stations_geojson, name='all_stations_geojson'),

]