from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Offer
from .serializers import OfferSerializer
from .permissions import IsLenderOrReadOnly
from token_auth.auth import TokenAuthentication

User = get_user_model()


class OfferViewSet(ModelViewSet):
    """View that takes care of CRUD operations
    on Offer model"""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLenderOrReadOnly]

    def perform_create(self, serializer):
        # Set lender to be currently authenticated user.
        serializer.validated_data['lender'] = self.request.user
        serializer.save()
