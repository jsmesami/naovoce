from django.urls import path

from .views import HerbariumList

urlpatterns = [
    path('', HerbariumList.as_view(), name='herbarium-list'),
]
