from django.urls import path

from .views import UserSignup, UserSignupFacebook

urlpatterns = [
    path("", UserSignup.as_view(), name="signup"),
    path("facebook/", UserSignupFacebook.as_view(), name="signup-fcb"),
]
