from django.urls import path

from .views import (
    ChangePasswordView,
)

urlpatterns = [
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
]
