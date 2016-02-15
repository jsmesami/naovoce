from django.conf.urls import patterns, url


from .views import FruitList, FruitDetail, KindList

urlpatterns = patterns(
    '',
    url(r'^$', FruitList.as_view(), name='fruit-list'),
    url(r'^(?P<pk>\d+)/$', FruitDetail.as_view(), name='fruit-detail'),
    url(r'^kinds/$', KindList.as_view(), name='kinds-list'),
)
