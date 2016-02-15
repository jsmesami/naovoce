from django.conf.urls import patterns, url


from .views import HerbariumList

urlpatterns = patterns(
    '',
    url(r'^$', HerbariumList.as_view(), name='herbarium-list'),
)
