from django.conf.urls import patterns, url

from .views import ImageDetail, ImageList


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', ImageDetail.as_view(), name='image-detail'),
    url(r'^(?P<gallery_ct>[a-z]+)/(?P<gallery_id>\d+)/$', ImageList.as_view(), name='image-list'),
)
