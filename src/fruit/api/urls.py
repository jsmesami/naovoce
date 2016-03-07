from django.conf.urls import patterns, url

from .views import FruitList, FruitDetail, KindList, fruit_list_diff


urlpatterns = patterns(
    '',
    url(r'^$', FruitList.as_view(), name='fruit-list'),
    url(r'^(?P<pk>\d+)/$', FruitDetail.as_view(), name='fruit-detail'),
    url(r'^since/(?P<since>\d{4}-\d{2}-\d{2})/$', fruit_list_diff, name='fruit-diff'),
    url(r'^kinds/$', KindList.as_view(), name='kinds-list'),
)
