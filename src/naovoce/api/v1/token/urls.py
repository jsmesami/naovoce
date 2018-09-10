from django.conf.urls import url

from .views import GetAuthToken, GetAuthTokenFacebook

urlpatterns = [
    url(r'^$', GetAuthToken.as_view()),
    url(r'^facebook/$', GetAuthTokenFacebook.as_view()),
]
