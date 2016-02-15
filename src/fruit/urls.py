from django.conf.urls import url

from . import views as fruit


urlpatterns = [
    url(r'^add/$', fruit.add, name='add'),
    url(r'^edit/(?P<fruit_id>[0-9]+)/$', fruit.edit, name='edit'),
    url(r'^delete/(?P<fruit_id>[0-9]+)/$', fruit.delete, name='delete'),
    url(r'^detail/(?P<fruit_id>[0-9]+)/$', fruit.detail, name='detail'),
]
