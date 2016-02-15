from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^save/$', views.save, name='save'),
]
