from django.conf.urls import patterns, url

from .views import UserSignupFacebook


urlpatterns = patterns(
    '',
    url(r'^facebook/$', UserSignupFacebook.as_view(), name='signup-fcb'),
)
