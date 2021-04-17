from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OfferViewSet

# Router will automatically create urls for
# view endpoints.
router = DefaultRouter()
router.register('', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
