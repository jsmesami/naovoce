from django.urls import include, path, re_path

from .views import api_handler_404, api_root

app_name = "naovoce"

urlpatterns = [
    path("", api_root, name="root"),
    path("fruit/", include("naovoce.api.v1.fruit.urls")),
    path("herbarium/", include("naovoce.api.v1.herbarium.urls")),
    path("users/", include("naovoce.api.v1.users.urls")),
    path("images/", include("naovoce.api.v1.images.urls")),
    path("signup/", include("naovoce.api.v1.signup.urls")),
    path("token/", include("naovoce.api.v1.token.urls")),
    re_path(r"^.*", api_handler_404),
]
