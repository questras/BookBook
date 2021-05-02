from django.urls import path

from .views import (
    ChangePasswordView,
    UserProfileView,
)

urlpatterns = [
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
