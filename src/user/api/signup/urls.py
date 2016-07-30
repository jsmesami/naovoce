from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.UserSignup.as_view(), name='signup'),
    url(r'^facebook/$', views.UserSignupFacebook.as_view(), name='signup-fcb'),
)
