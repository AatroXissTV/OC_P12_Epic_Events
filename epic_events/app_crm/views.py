# app_crm/views.py
# created 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 10/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.2"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

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
        if self.request.user.role == 'sales':
            prospects = Customer.objects.filter(is_customer=False)
            own_customers = Customer.objects.filter(
                is_customer=True,
                sales_contact_id=self.request.user
            )
            customers = Customer.objects.all()
            return prospects | own_customers | customers
        elif self.request.user.role == 'support':
            return Customer.objects.filter(is_customer=True)
        else:
            return Customer.objects.all()


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
        else:
            return Contract.objects.all()


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
