# app_crm/permissions.py
# created 18/03/2022 at 15:05 by Antoine 'AatroXiss' BEAUDESSON
# last modified 28/03/2022 at 12:10 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/permissions.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.25"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework.permissions import BasePermission

# django imports

# local application imports

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


class CandEditCustomer(BasePermission):
    """
    Only sales and management(superuser)
    can edit a customer object
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            if request.user.role == 'support':
                return False
            if request.user.role == 'sales':
                if obj.is_customer is False:
                    return True
                else:
                    return (obj.sales_contact_id == request.user.id)
            return True

        if request.method == 'DELETE':
            return request.user.role == 'management'


class CanEditContract(BasePermission):
    """
    Allows only sales contact and management(superuser)
    to update a contract
    Only management(superuser) can delete a contract
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            if request.user.role == 'support':
                return False
            if request.user.role == 'sales':
                if obj.customer.sales_contact_id == request.user:
                    return True
                else:
                    return False
            return True

        if request.method == 'DELETE':
            return request.user.role == 'management'


class CanUpdateEvent(BasePermission):
    """
    Allows only support, sales of customer and management(superuser)
    to update an event
    Only management(superuser) can delete an event
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            if request.user.role == 'support':
                return obj.contract_id.support_contact_id == request.user
            if request.user.role == 'sales':
                return obj.contract_id.customer.sales_contact_id == request.user  # noqa
            if request.user.role == 'management':
                return True
            else:
                return False

        if request.method == 'DELETE':
            return request.user.role == 'management'
