from django.conf.urls import url
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout$', logout, {'next_page': 'auth:login'}, name='logout'),
]
