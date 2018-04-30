from django.conf.urls import url
from .import views


#dashboard
urlpatterns = [

	url(r'^index$', views.index, name='index'),
	url(r'^mapainteractivo', views.mapainteractivo, name='mapainteractivo'),
	url(r'^mapainteractivo/voronoi', views.mapainteractivo, name='mapainteractivo_voronoi'),
	url(r'^point.geojson', views.getgeojson, name='getgeojson'),

	#url(r'^mapainteractivo/$', views.mapainteractivo, name='principal.mapainteractivo'),
]