from django.conf.urls import patterns, url

from .views import UserList, UserListTop, UserListTopLastMonth, UserDetail


urlpatterns = patterns(
    '',
    url(r'^$', UserList.as_view(), name='users-list'),
    url(r'^top/$', UserListTop.as_view(), name='users-list-top'),
    url(r'^top/last-month/$', UserListTopLastMonth.as_view(), name='users-list-top-last-month'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='users-detail'),
)
