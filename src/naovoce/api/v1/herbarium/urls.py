from django.conf.urls import url

from .views import HerbariumList

urlpatterns = [
    url(r'^$', HerbariumList.as_view(), name='herbarium-list'),
]
