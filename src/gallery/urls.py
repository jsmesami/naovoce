from django.conf.urls import url

from . import views as images


urlpatterns = [
    url(r'^(?P<gallery_ct>[a-z]+)/(?P<gallery_id>\d+)/$', images.Index.as_view(), name='index'),
    url(r'^(?P<gallery_ct>[a-z]+)/(?P<gallery_id>\d+)/(?P<image_id>\d+)/$', images.Browser.as_view(), name='browser'),
]
