from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .models import Offer, OfferImage
from .serializers import OfferSerializer, OfferImageSerializer, OfferSearchSerializer
from .permissions import IsLenderOrReadOnly, IsImageOfferLenderOrReadOnly
from .filters import OfferSearchFilter
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


class OfferSearchView(ListAPIView):
    """View that allows user to perform a smart search of active
    offers based on book title, book's author etc.
    Under the hood it used PostgreSQL's full-text search and trigram similar
    features, so user's query may be inaccurate, but will work just fine."""

    queryset = Offer.objects.filter(status=Offer.Status.ACTIVE)
    serializer_class = OfferSearchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferSearchFilter
