from django.conf.urls import url

from .views import UserList, UserListTop, UserListTopLastMonth, UserDetail


urlpatterns = [
    url(r'^$', UserList.as_view(), name='users-list'),
    url(r'^top/$', UserListTop.as_view(), name='users-list-top'),
    url(r'^top/last-month/$', UserListTopLastMonth.as_view(), name='users-list-top-last-month'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='users-detail'),
]
