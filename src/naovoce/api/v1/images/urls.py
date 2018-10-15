from django.urls import path

from .views import ImageDetail, ImageList

urlpatterns = [
    path('<int:pk>/', ImageDetail.as_view(), name='image-detail'),
    path('<slug:gallery_ct>/<int:gallery_id>)/', ImageList.as_view(), name='image-list'),
]
