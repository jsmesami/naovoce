from django.conf.urls import patterns, url


from .views import UserList, UserDetail

urlpatterns = patterns(
    '',
    url(r'^$', UserList.as_view(), name='users-list'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='users-detail'),
)
