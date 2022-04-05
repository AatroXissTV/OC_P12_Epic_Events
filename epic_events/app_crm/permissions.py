# app_crm/permissions.py
# created 18/03/2022 at 15:05 by Antoine 'AatroXiss' BEAUDESSON
# last modified 30/03/2022 at 12:50 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/permissions.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.2"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework.permissions import BasePermission

# django imports

# local application imports

# other imports & constants


class CanAccess(BasePermission):
    """
    Only allow authenticated users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CustomerPermissions(BasePermission):
    """
    This class makes sure that every authenticated user can access the data
    in read-only mode.
    If the user is a 'sales' or 'management' user, he can update the customer
    For 'sales' they can only access prospects and their own customers
    And only management can delete the customer
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role == 'support':
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            if request.user.role == 'management':
                return True
            if request.user.role == 'sales':
                if obj.is_customer is False:
                    return True
                return (obj.sales_contact_id == request.user)
        if request.method == 'DELETE':
            return request.user.role == 'management'
        return False


class ContractPermissions(BasePermission):
    """
    This class makes sure that every authenticated user can access the data
    in read-only mode.
    If the user is a 'sales' or 'management' user, he can update the contract
    For 'sales' they can only access their own contracts
    Delete is not allowed
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.role == 'support':
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            if request.user.role == 'management':
                return True
            if request.user.role == 'sales':
                return (obj.customer.sales_contact_id == request.user)
        return False


class EventPermissions(BasePermission):
    """
    This class makes sure that every authenticated user can access the data
    in read-only mode.
    Every user can create an event but only for signed contracts
    'sales' and 'support' can also update events but only if it's not finished
    and they are one of the contacts.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'POST' or request.method == 'PUT':
            if request.user.role == 'management':
                return True
            if request.user.role == 'sales':
                return obj.contract_id.customer.sales_contact_id == request.user  # noqa
            if request.user.role == 'support':
                return obj.contract_id.customer.support_contact_id == request.user  # noqa
        if request.method == 'DELETE':
            if obj.is_finished is False:
                return request.user.role == 'management'
        return False
