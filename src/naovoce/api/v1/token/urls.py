from django.urls import path

from .views import GetAuthToken, GetAuthTokenFacebook

urlpatterns = [
    path('', GetAuthToken.as_view()),
    path('facebook/', GetAuthTokenFacebook.as_view()),
]
