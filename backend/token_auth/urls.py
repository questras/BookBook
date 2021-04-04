from django.urls import path

from . import views

urlpatterns = [
    path('acquire_token', views.AcquireTokenView.as_view(), name='acquire_token'),
    path('revoke_token', views.RevokeTokenView.as_view(), name='revoke_token'),
    path('renew_token', views.RenewTokenView.as_view(), name='renew_token'),
    path('register', views.RegistrationView.as_view(), name='register'),
]
