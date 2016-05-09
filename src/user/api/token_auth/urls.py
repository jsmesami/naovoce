from django.conf.urls import patterns, url


from .views import GetAuthToken, GetAuthTokenFacebook

urlpatterns = patterns(
    '',
    url(r'^$', GetAuthToken.as_view()),
    url(r'^facebook/$', GetAuthTokenFacebook.as_view()),
)
