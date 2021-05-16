from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from token_auth.auth import TokenAuthentication
from offers.models import Offer

from .models import Request
from .permissions import IsLender, IsOfferLender
from .serializers import RequestSerializer


def finish_request(request):
    with transaction.atomic():
        request.refresh_from_db()
        offer = request.offer

        if request.status != Request.Status.APPROVED:
            raise serializers.ValidationError('Request must be approved in order to be finished.')

        request.status = Request.Status.FINISHED
        offer.status = Offer.Status.RETURNED

        request.save()
        offer.save()


def reject_request(request):
    with transaction.atomic():
        request.refresh_from_db()

        if request.status != Request.Status.PENDING:
            raise serializers.ValidationError('Request must be pending in order to be rejected')

        request.status = Request.Status.REJECTED
        request.save()


def accept_request(request):
    with transaction.atomic():
        request.refresh_from_db()
        offer = request.offer

        if offer.status != Offer.Status.ACTIVE:
            raise serializers.ValidationError('Offer must be active in order to accept request')

        if request.status != Request.Status.PENDING:
            raise serializers.ValidationError('Request must be pending in order to get accepted')

        offer.status = Offer.Status.LENT
        request.status = Request.Status.APPROVED

        offer.save()
        request.save()


class RequestViewSet(ModelViewSet):
    """View that takes care of CRUD operations and state changing of Request model"""

    serializer_class = RequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'offer']
    ordering_fields = ['created', 'updated']

    def get_queryset(self):
        if self.request.method == 'POST':
            return Request.objects.all()
        else:
            return Request.objects.filter(requester=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['requester'] = self.request.user

        if serializer.validated_data['requester'] == serializer.validated_data['offer'].lender:
            raise serializers.ValidationError('Cannot make request for own offer.')

        serializer.save()

    def perform_destroy(self, instance):
        if instance.status != Request.Status.PENDING:
            raise serializers.ValidationError('Cannot delete non-pending request.')

        instance.delete()

    @action(methods=['post'], detail=True, permission_classes=[IsOfferLender], url_path='reject', url_name='reject_request')
    def reject(self, request, pk=None):
        request = self.get_object()
        reject_request(request)
        serializer = self.get_serializer(request, many=False)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsOfferLender], url_path='finish', url_name='finish_request')
    def finish(self, request, pk=None):
        request = self.get_object()
        finish_request(request)
        serializer = self.get_serializer(request, many=False)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsOfferLender], url_path='accept', url_name='accept_request')
    def accept(self, request, pk=None):
        request = self.get_object()
        accept_request(request)
        serializer = self.get_serializer(request, many=False)
        return Response(serializer.data)


class ListOfferRequestsView(ListAPIView):
    """View that returns list of requests of given offer."""

    serializer_class = RequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLender]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created', 'updated']

    def get_queryset(self):
        return Request.objects.filter(offer=self.kwargs['pk'])
