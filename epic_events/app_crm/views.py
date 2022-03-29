# app_crm/views.py
# created 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 29/03/2022 at 10:49 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.1"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from django.core.exceptions import (
    PermissionDenied
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# django imports

# local application imports
from .models import (
    Customer,
    Contract,
    Event
)
from .serializers import (
    CustomerSerializer,
    ContractSerializer,
    EventSerializer
)
from .permissions import (
    CanCreate,
    CanUpdateEvent,
    CandEditCustomer,
    CanEditContract
)

# other imports & constants


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, CanCreate,
                          CandEditCustomer]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^last_name', '^email']
    filterset_fields = ['is_customer']

    def get_queryset(self):
        if self.request.user.role == 'sales':
            prospects = Customer.objects.filter(is_customer=False)
            own_customers = Customer.objects.filter(sales_contact_id=self.request.user.id)  # noqa
            return prospects | own_customers
        elif self.request.user.role == 'support':
            return Customer.objects.filter(contract__support_contact_id=self.request.user.id)  # noqa
        return Customer.objects.all()

    def perform_create(self, serializer):
        serializer.save(sales_contact_id=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Override the default update method to prevent the sales contact from
        changing the status of a customer to prospect.
        """
        customer = self.get_object()
        if customer.is_customer is True:
            if serializer.validated_data.get('is_customer') is False:
                raise PermissionDenied('You cannot change customer to prospect')  # noqa
        serializer.save(sales_contact_id=self.request.user)
        return Response(serializer.data)


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, CanCreate,
                          CanEditContract]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^customer__last_name', '^customer__email'
                     '=date_created', '=amount']
    filterset_fields = ['is_signed']

    def get_queryset(self):
        if self.request.user.role == 'sales':
            return Contract.objects.filter(customer__sales_contact_id=self.request.user)  # noqa
        elif self.request.user.role == 'support':
            return Contract.objects.filter(support_contact_id=self.request.user)  # noqa
        return Contract.objects.all()

    def perform_create(self, serializer):
        """
        Override the default create method to prevent the sales contact or
        management to create a contract with a prospect.
        """
        if serializer.validated_data.get('customer').is_customer is False:
            raise PermissionDenied('You cannot create a contract with a prospect')  # noqa
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Override the default update method to prevent the sales contact or
        management to change the status of a signed contracts.
        """
        contract = self.get_object()
        if contract.is_signed is True:
            if serializer.validated_data.get('is_signed') is False:
                raise PermissionDenied('You cannot change signed contracts')
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.is_signed is True:
            raise PermissionDenied("Cannot delete signed contracts")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, CanUpdateEvent]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^customer__last_name', '^customer__email',
                     '=date_created']
    filterset_fields = ['is_finished']

    def get_queryset(self):
        if self.request.user.role == 'sales':
            return Event.objects.filter(contract_id__customer__sales_contact_id=self.request.user)  # noqa
        elif self.request.user.role == 'support':
            return Event.objects.filter(contract_id__support_contact_id=self.request.user)  # noqa
        return Event.objects.all()

    def perform_create(self, serializer):
        """
        Override the default create method to prevent the sales contact or
        management to create an event with a prospect.
        """
        if serializer.validated_data.get('contract_id').customer.is_customer is False:  # noqa
            raise PermissionDenied('You cannot create an event with a prospect')  # noqa
        if serializer.validated_data.get('contract_id').is_signed is False:
            raise PermissionDenied('You cannot create an event with a contract not signed')  # noqa
        # you can't create an event for a contract that has already an event
        if Event.objects.filter(contract_id=serializer.validated_data.get('contract_id')).exists():  # noqa
            raise PermissionDenied('You cannot create an event for a contract that already has an event')  # noqa
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Override the default update method to prevent the sales contact or
        management to change the status of a finished event.
        """
        event = self.get_object()
        if event.is_finished is True:
            if serializer.validated_data.get('is_finished') is False:
                raise PermissionDenied('You cannot change finished events')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if instance.is_finished is True:
            raise PermissionDenied("Cannot delete finished events")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
