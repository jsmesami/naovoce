from django.urls import path

from .views import UserDetail, UserList, UserListTop, UserListTopLastMonth

urlpatterns = [
    path("", UserList.as_view(), name="users-list"),
    path("top/", UserListTop.as_view(), name="users-list-top"),
    path(
        "top/last-month/",
        UserListTopLastMonth.as_view(),
        name="users-list-top-last-month",
    ),
    path("<int:pk>/", UserDetail.as_view(), name="users-detail"),
]
