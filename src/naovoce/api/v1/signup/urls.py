from django.urls import path
from naovoce.api.v1.signup import views

urlpatterns = [
    path('', views.UserSignup.as_view(), name='signup'),
    path('facebook/', views.UserSignupFacebook.as_view(), name='signup-fcb'),
]
