from django.conf.urls import include, url

from .views import api_root, api_handler_404


app_name = "naovoce"

urlpatterns = [
    url(r'^$', api_root, name='root'),
    url(r'^fruit/', include('naovoce.api.v1.fruit.urls')),
    url(r'^herbarium/', include('naovoce.api.v1.herbarium.urls')),
    url(r'^users/', include('naovoce.api.v1.users.urls')),
    url(r'^images/', include('naovoce.api.v1.images.urls')),
    url(r'^signup/', include('naovoce.api.v1.signup.urls')),
    url(r'^token/', include('naovoce.api.v1.token.urls')),
    url(r'^.*', api_handler_404),
]
