# app_crm/views.py
# created 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 18/03/2022 at 10:49 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.13"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
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

# other imports & constants


class CustomerList(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^first_name', '^last_name', '^email']

    def get_queryset(self):
        if self.request.user.role == 'management':
            return Customer.objects.all()
        elif self.request.user.role == 'sales':
            prospects = Customer.objects.filter(is_customer=False)
            own_customers = Customer.objects.filter(
                is_customer=True,
                sales_contact_id=self.request.user.id
            )
            return prospects | own_customers
        elif self.request.user.role == 'support':
            return Customer.objects.filter(
                contract__support_contact_id=self.request.user.id
            )
        else:
            return Response(
                {'detail': 'You are not allowed to access this resource.'},
                status=status.HTTP_403_FORBIDDEN
            )

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['is_customer'] is True:
                serializer.validated_data['sales_contact_id'] = self.request.user  # noqa
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    http_method_names = ['get', 'put', 'delete']
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def update(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            customer = self.get_object()
            if customer.is_customer is True:
                if serializer.validated_data['is_customer'] is False:
                    return Response(
                        {'detail': 'You cannot change the customer status.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            elif customer.is_customer is False:
                if serializer.validated_data['is_customer'] is True:
                    serializer.validated_data['sales_contact_id'] = self.request.user  # noqa

            # problem on saving a PUT request
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractList(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^customer__first_name', '^customer__last_name',
                     '^customer__email', '=date_created', '=amount']

    def get_queryset(self):
        if self.request.user.role == 'sales':
            return Contract.objects.filter(
                customer__sales_contact_id=self.request.user)
        elif self.request.user.role == 'support':
            return Contract.objects.filter(
                support_contact_id=self.request.user)
        elif self.request.user.role == 'management':
            return Contract.objects.all()
        else:
            return Response(
                {'detail': 'You are not allowed to access this resource.'},
                status=status.HTTP_403_FORBIDDEN
            )

    def post(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['sales_contact_id'] = request.user # noqa
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^customer__first_name', '^customer__last_name',
                     '^customer__email', '=date_created']

    def get_queryset(self):
        if self.request.user.role == 'sales':
            return Event.objects.filter(
                contract_id__customer__sales_contact_id=self.request.user)
        elif self.request.user.role == 'support':
            return Event.objects.filter(
                contract_id__support_contact_id=self.request.user)
        else:
            return Event.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        contract = generics.get_object_or_404(Contract, id=data['contract_id'])
        if contract.is_signed is False:
            return Response(
                {'error': 'Contract is not signed'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
