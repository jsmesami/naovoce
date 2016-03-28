from django.conf.urls import url

from . import views as user


urlpatterns = [
    url(r'^index/$', user.index, name='index'),
    url(r'^(?P<pk>\d+)(?:-(?P<slug>[^/]+))?/$', user.profile, name='detail'),
    url(r'^(?P<pk>\d+)/settings/$', user.UserSettingsView.as_view(), name='settings'),
    url(r'^(?P<pk>\d+)/messages/$', user.messages, name='messages'),
]
