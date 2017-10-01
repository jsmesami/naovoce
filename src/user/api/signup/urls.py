from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.UserSignup.as_view(), name='signup'),
    url(r'^facebook/$', views.UserSignupFacebook.as_view(), name='signup-fcb'),
]
