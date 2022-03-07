# app_crm/serializers.py
# created 07/03/2022 at 09:10 by Antoine 'AatroXiss' BEAUDESSON
# last modified 07/03/2022 at 09:10 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/serializers.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.13"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework import serializers

# django imports

# local application imports
from .models import (
    Customer,
    Contract,
    Event
)

# other imports & constants


class CustomerSerializer(serializers.ModelSerializer):
    """
    This class is the serializer that helps translating Customer objects
    into JSON.

    Serialize every field of the Customer model.
    Define id, date_created and date_updated fields as read-only.
    """

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'date_updated')


class ContractSerializer(serializers.ModelSerializer):
    """
    This class is the serializer that helps translating Contract objects
    into JSON.

    Serialize every field of the Contract model.
    Define id, date_created and date_updated fields as read-only.
    """

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'date_updated')


class EventSerializer(serializers.ModelSerializer):
    """
    This class is the serializer that helps translating Event objects
    into JSON.

    Serialize every field of the Event model.
    Define id, date_created and date_updated fields as read-only.
    """

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'date_updated')
