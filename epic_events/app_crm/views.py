# app_crm/views.py
# created 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 21/03/2022 at 14:26 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.17"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
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
    ContractPermissions,
    CustomerPermissions,
    EventPermissions,
)

# other imports & constants


class CustomerList(generics.ListCreateAPIView):
    """
    This endpoint handles
    the GET and POST requests for the Customer endpoint.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, CustomerPermissions]
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

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['is_customer'] is True:
                serializer.validated_data['sales_contact_id'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint handles
    the GET, PUT and DELETE requests for the Customer endpoint.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, CustomerPermissions]
    http_method_names = ['get', 'put', 'delete']

    def put(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            customer = self.get_object()
            if customer.is_customer is True and serializer.validated_data['is_customer'] is False:  # noqa
                return Response({"error": "Cannot change to prospect"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif serializer.validated_data['is_customer'] is True:
                serializer.validated_data['sales_contact_id'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractList(generics.ListCreateAPIView):
    """
    This endpoint handles
    the GET and POST requests for the Contract endpoint.
    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
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

    def post(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['customer'].sales_contact_id = request.user  # noqa
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint handles
    the GET, PUT and DELETE requests for the Contract endpoint.
    """
    queryset = Contract.objects.all()
    http_method_names = ['get', 'put', 'delete']
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]


class EventList(generics.ListCreateAPIView):
    """
    This endpoint handles
    the GET and POST requests for the Event endpoint.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
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

    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            contract = generics.get_object_or_404(Contract, pk=serializer.validated_data['contract_id'])  # noqa
            if contract.is_signed is False:
                return Response({"error": "Contract is not signed"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(generics.RetrieveUpdateAPIView):
    """
    This endpoint handles
    the GET, PUT and DELETE requests for the Event endpoint.
    """
    queryset = Event.objects.all()
    http_method_names = ['get', 'put', 'delete']
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermissions]

    def put(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = EventSerializer(data=request.data, instance=event)

        if serializer.is_valid(raise_exception=True):
            if request.user.role == 'support' and serializer.validated_data['contract_id'] != event.contract_id.id:  # noqa
                return Response({"error": "You cannot update this event"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
