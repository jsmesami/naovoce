from django.conf.urls import url

from .views import fruit_list_diff, FruitComplaint, FruitDetail, FruitList, KindList

urlpatterns = [
    url(r'^$', FruitList.as_view(), name='fruit-list'),
    url(r'^(?P<pk>\d+)/$', FruitDetail.as_view(), name='fruit-detail'),
    url(r'^(?P<pk>\d+)/complaint/$', FruitComplaint.as_view(), name='fruit-complaint'),
    url(r'^since(?:/(?P<date>\d{4}-\d{2}-\d{2}))?(?:/(?P<time>\d{2}:\d{2}:\d{2}))?/$',
        fruit_list_diff, name='fruit-diff'),
    url(r'^kinds/$', KindList.as_view(), name='kinds-list'),
]
