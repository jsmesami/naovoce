from django.urls import include, path, re_path

from .views import api_handler_404, api_root

app_name = "naovoce"

urlpatterns = [
    path(r'', api_root, name='root'),
    path(r'fruit/', include('naovoce.api.v1.fruit.urls')),
    path(r'herbarium/', include('naovoce.api.v1.herbarium.urls')),
    path(r'users/', include('naovoce.api.v1.users.urls')),
    path(r'images/', include('naovoce.api.v1.images.urls')),
    path(r'signup/', include('naovoce.api.v1.signup.urls')),
    path(r'token/', include('naovoce.api.v1.token.urls')),
    re_path(r'^.*', api_handler_404),
]
