from django.conf.urls import include, url

from .views import api_root, api_handler_404


urlpatterns = [
    url(r'^$', api_root, name='root'),
    url(r'^fruit/', include('fruit.api.urls')),
    url(r'^herbarium/', include('fruit.herbarium.api.urls')),
    url(r'^users/', include('user.api.urls')),
    url(r'^images/', include('gallery.api.urls')),
    url(r'^signup/', include('user.api.signup.urls')),
    url(r'^token/', include('user.api.token_auth.urls')),
    url(r'^.*', api_handler_404),
]
