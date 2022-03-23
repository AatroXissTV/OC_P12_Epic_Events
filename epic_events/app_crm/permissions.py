# app_crm/permissions.py
# created 18/03/2022 at 15:05 by Antoine 'AatroXiss' BEAUDESSON
# last modified 23/03/2022 at 11:19 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/permissions.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.21"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework.permissions import BasePermission

# django imports

# local application imports
from .models import (
    Customer,
    Contract,
)

# other imports & constants


class CanCreate(BasePermission):
    """
    Allows only sales and management(superuser)
    to add an object
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role == 'support':
                return False
        return True


class CanEditCustomerOrContract(BasePermission):
    """
    Allows only sales contact and management(superuser)
    to update a customer or contract
    Only management(superuser) can delete a customer or contract
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            if obj == Customer:
                return (obj.sales_contact_id == request.user
                        or request.user.role == 'management')
            if obj == Contract:
                return (obj.customer.sales_contact_id == request.user
                        or request.user.role == 'management')

        if request.method == 'DELETE':
            return request.user.role == 'management'

        return True


class CanUpdateEvent(BasePermission):
    """
    Allows only support, sales of customer and management(superuser)
    to update an event
    Only management(superuser) can delete an event
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return (obj.contract_id.support_contact_id == request.user
                    or obj.contract_id.customer.sales_contact_id == request.user  # noqa
                    or request.user.role == 'management')

        if request.method == 'DELETE':
            return request.user.role == 'management'

        return True
