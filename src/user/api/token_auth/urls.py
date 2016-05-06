from django.conf.urls import patterns, url


from .views import GetAuthToken

urlpatterns = patterns(
    '',
    url(r'^$', GetAuthToken.as_view()),
)
