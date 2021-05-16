from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ListOfferRequestsView, RequestViewSet

request_router = DefaultRouter()
request_router.register('requests', RequestViewSet, basename='Request')

urlpatterns = [
    path('', include(request_router.urls)),
    path('offers/<int:pk>/requests/', ListOfferRequestsView.as_view(), name='offer_requests'),
]
