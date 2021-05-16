from django.urls import path

from .views import (
    ChangePasswordView,
    UserProfileView,
    RegistrationView,
    MyProfileView
)

urlpatterns = [
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('my_profile/', MyProfileView.as_view(), name='my-profile'),
    path('register', RegistrationView.as_view(), name='register'),
]
