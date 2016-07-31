from django.conf.urls import patterns, url


from .views import PagesList

urlpatterns = patterns(
    '',
    url(r'^$', PagesList.as_view(), name='staticpages-list'),
)
