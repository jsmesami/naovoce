from django.conf.urls import url

from . import views as herbarium


urlpatterns = [
    url(r'^$', herbarium.index, name='index'),
    url(r'^filter/(?P<cls>\d{4})(?:-(?P<slug>[^/]+))?/$', herbarium.index, name='filter'),
    url(r'^(?P<pk>\d+)(?:-(?P<slug>[^/]+))?/$', herbarium.detail, name='detail'),
]
