from django.conf.urls import url
from .import views


#BASE = 'suelo/'

urlpatterns = [

url(r'index$', views.index, name='index'),

url(r'thiessen$', views.thiessen, name='thiessen'),


# ---------------------------------------------------------------------------------------
# ----------------------------------- JSON ----------------------------------------------
# ---------------------------------------------------------------------------------------
url(r'muestras_perfil_with_code_json$', views.muestras_perfil_with_code_json, name='muestras_perfil_with_code_json'),

url(r'muestra_with_muesid_json$', views.muestra_with_muesid_json, name='muestra_with_muesid_json'),

url(r'variables_prop_metales_pesados_json$', views.variables_prop_metales_pesados_json, name='variables_prop_metales_pesados_json'),




# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------

url(r'all_perfiles_geojson$', views.all_perfiles_geojson, name='all_perfiles_geojson'),

url(r'all_muestras_geojson$', views.all_muestras_geojson, name='all_muestras_geojson'),






]