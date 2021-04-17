from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLenderOrReadOnly(BasePermission):
    """Custom permission to allow only lenders that own 
    an offer to edit it."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.lender == request.user
