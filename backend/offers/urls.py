from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, OfferImageViewSet, OfferSearchView

# Router will automatically create urls for
# view endpoints.
offers_router = DefaultRouter()
offers_router.register('offers', OfferViewSet)

images_router = DefaultRouter()
images_router.register('offer_images', OfferImageViewSet)

urlpatterns = [
    path('', include(offers_router.urls)),
    path('', include(images_router.urls)),
    path('offer_search', OfferSearchView.as_view(), name='offer_search')
]
