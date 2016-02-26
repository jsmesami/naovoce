from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views

from .views import api_root, api_handler_404


urlpatterns = patterns(
    '',
    url(r'^$', api_root),
    url(r'^fruit/', include('fruit.api.urls')),
    url(r'^herbarium/', include('fruit.herbarium.api.urls')),
    url(r'^users/', include('user.api.urls')),
    url(r'^images/', include('gallery.api.urls')),
    url(r'^token/', views.obtain_auth_token),
    url(r'^.*', api_handler_404),
)
