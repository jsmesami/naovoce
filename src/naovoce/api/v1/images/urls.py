from django.urls import path

from .views import ImageDetail, ImageList

urlpatterns = [
    path('<int:pk>/', ImageDetail.as_view(), name='image-detail'),
    path('fruit/<int:fruit_pk>/', ImageList.as_view(), name='image-list'),
]
