from django.urls import path, re_path

from .views import fruit_list_diff, FruitComplaint, FruitDetail, FruitList, KindList

urlpatterns = [
    path(r'', FruitList.as_view(), name='fruit-list'),
    path('<int:pk>/', FruitDetail.as_view(), name='fruit-detail'),
    path('<int:pk>/complaint/', FruitComplaint.as_view(), name='fruit-complaint'),
    re_path(r'^since(?:/(?P<date>\d{4}-\d{2}-\d{2}))(?:/(?P<time>\d{2}:\d{2}:\d{2}))?/$',
            fruit_list_diff, name='fruit-diff'),
    path('kinds/', KindList.as_view(), name='kinds-list'),
]