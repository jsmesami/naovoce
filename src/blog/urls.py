from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filter/(?P<category_pk>\d+)(?:-(?P<category_slug>[^/]+))?/$',
        views.index, name='category'),
    url(r'^(?P<pk>\d+)(?:-(?P<slug>[^/]+))?/$', views.detail, name='detail'),
]
