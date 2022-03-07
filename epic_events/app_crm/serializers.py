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
__version__ = "0.0.10"
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
    pass


class ContractSerializer(serializers.ModelSerializer):
    pass


class EventSerializer(serializers.ModelSerializer):
    pass
