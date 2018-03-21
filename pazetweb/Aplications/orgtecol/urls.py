from django.conf.urls import url
from .import views



#BASE = 'orgtecol/'

urlpatterns = [



# ---------------------------------------------------------------------------------------
# ------------------------------------- JSON --------------------------------------------
# ---------------------------------------------------------------------------------------
url(r'depto_query_string_json$', views.depto_query_string_json, name='depto_query_string_json'),
url(r'mun_query_string_json$', views.mun_query_string_json, name='mun_query_string_json'),



]