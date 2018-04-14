from django.conf.urls import url
from .import views



#BASE = 'clima/'
urlpatterns = [

url(r'index$', views.index, name='index'),

]

