from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404

from offers.models import Offer


class IsOfferLender(BasePermission):
    """Custom permission to allow only lenders that own 
    an offer to edit request."""

    def has_object_permission(self, request, view, obj):
        return obj.offer.lender == request.user


class IsLender(BasePermission):
    """Custom permission to allow only lenders that own 
    an offer to list all requests."""

    def has_permission(self, request, view):
        offer = get_object_or_404(Offer, pk=view.kwargs['pk'])
        return offer.lender == request.user and super().has_permission(request, view)
