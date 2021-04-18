from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404

from offers.models import Offer


class IsLenderOrReadOnly(BasePermission):
    """Custom permission to allow only lenders that own 
    an offer to edit it."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.lender == request.user


class IsImageOfferLenderOrReadOnly(BasePermission):
    """Custom permission to allow only lender that own
    an offer that is bound to an image to edit this image."""

    def has_permission(self, request, view):
        if request.method == 'POST' and 'offer' in request.POST.keys():
            offer = get_object_or_404(Offer, pk=request.POST.get('offer'))
            return offer.lender == request.user

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.offer.lender == request.user
