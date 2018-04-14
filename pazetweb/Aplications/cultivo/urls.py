from django.conf.urls import url
from .import views


#BASE = 'cultivo/'

urlpatterns = [

url(r'index$', views.index, name='index'),
url(r'herbaseos_frutas_granos$', views.herbaseos_frutas_granos, name='herbaseos_frutas_granos'),
url(r'herbaseos_vegetales_hoja$', views.herbaseos_vegetales_hoja, name='herbaseos_vegetales_hoja'),
url(r'herbaseos_raices_tuberculos$', views.herbaseos_raices_tuberculos, name='herbaseos_raices_tuberculos'),
url(r'herbaseos_cultivos_forrajeros$', views.herbaseos_cultivos_forrajeros, name='herbaseos_cultivos_forrajeros'),
url(r'arboreos$', views.arboreos, name='arboreos'),


# ---------------------------------------------------------------------------------------
# ----------------------------------- JSON ----------------------------------------------
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# -----------------------------------GEOJSON---------------------------------------------
# ---------------------------------------------------------------------------------------







]