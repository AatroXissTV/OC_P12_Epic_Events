# app_crm/views.py
# created 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 07/03/2022 at 09:22 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework import viewsets, status
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


class CustomerViewSet(viewsets.ModelViewSet):
    # API endpoint that allows customer to be created or viewed.
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request):
        data = request.data.copy()
        data['sales_contact_id'] = request.user.id
        data['is_customer'] = True

        serialized_data = CustomerSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,
                            status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ContractViewSet(viewsets.ModelViewSet):
    # API endpoint that allows contract to be created or viewed.
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def create(self, request, client_pk=None):
        data = request.data.copy()
        data['customer'] = client_pk

        serialized_data = ContractSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,
                            status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    # API endpoint that allows event to be created or viewed.
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, contract_pk=None):
        data = request.data.copy()
        data['contract_id'] = contract_pk

        serialized_data = EventSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,
                            status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)
