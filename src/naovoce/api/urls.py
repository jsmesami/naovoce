from django.conf.urls import patterns, url, include
from .views import api_root


urlpatterns = patterns(
    '',
    url(r'^$', api_root),
    url(r'^fruit/', include('fruit.api.urls')),
    url(r'^herbarium/', include('fruit.herbarium.api.urls')),
    url(r'^users/', include('user.api.urls')),
    url(r'^images/', include('gallery.api.urls')),
)
