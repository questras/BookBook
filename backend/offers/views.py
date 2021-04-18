from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .models import Offer, OfferImage
from .serializers import OfferSerializer, OfferImageSerializer
from .permissions import IsLenderOrReadOnly, IsImageOfferLenderOrReadOnly
from token_auth.auth import TokenAuthentication

User = get_user_model()


class OfferViewSet(ModelViewSet):
    """View that takes care of CRUD operations
    on Offer model"""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLenderOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def perform_create(self, serializer):
        # Set lender to be currently authenticated user.
        serializer.validated_data['lender'] = self.request.user
        serializer.save()


class OfferImageViewSet(ModelViewSet):
    """View that takes care of CRUD operations on
    OfferImage model"""

    queryset = OfferImage.objects.all()
    serializer_class = OfferImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsImageOfferLenderOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'delete', 'options']
