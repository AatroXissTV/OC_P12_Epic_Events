# app_crm/permissions.py
# created 18/03/2022 at 15:05 by Antoine 'AatroXiss' BEAUDESSON
# last modified 06/03/2022 at 12:33 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/permissions.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.8"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)

# django imports

# local application imports
from .models import (
    Customer,
)

# other imports & constants


class IsManagement(BasePermission):
    """
    The management role can only access data in read-only mode.
    Every modification should be done via the Admin interface.
    """

    def has_permission(self, request, view):
        return request.user.role == 'management' and request.method in SAFE_METHODS  # noqa

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CustomerPermissions(BasePermission):
    """
    Sales role: can CREATE new customers/prospects
                can VIEW and UPDATE any prospect and their own customers
                can DELETE prospects only
    Support role: can VIEW their own customers
    """
    def has_permission(self, request, view):
        if request.user.role == 'support':
            return request.method in SAFE_METHODS
        return request.user.role == 'sales'

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.role == 'sales' and obj.is_customer is False
        elif request.user.role == 'support' and request.method in SAFE_METHODS:
            return obj in Customer.objects.filter(
                contract__support_contact_id=request.user
            )
        return request.user == obj.sales_contact_id or obj.is_customer is False


class ContractPermissions(BasePermission):
    """
    Sales role: can CREATE new contracts
                can VIEW and UPDATE contracts of their own contracts if not signed  # noqa
    Support role: can VIEW contracts of their own customers
    """
    def has_permission(self, request, view):
        if request.user.role == 'support':
            return request.method in SAFE_METHODS
        return request.user.role == 'sales'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if request.user.role == 'support':
                return obj.support_contact_id == request.user
            return request.user == obj.customer.sales_contact_id
        elif request.method == 'PUT' and obj.is_signed is True:
            raise PermissionDenied('You cannot update a signed contract')
        return request.user == obj.customer.sales_contact_id and obj.is_signed is False  # noqa


class EventPermissions(BasePermission):
    """
    Sales role: can CREATE new events
                can VIEW events of their own customers
                can UPDATE events of their own customers if not finished
                can DELETE events of their own if not finished
    Support Role: can VIEW events of their own customers
                  can UPDATE events of their own customers if not finished
    """

    def has_permission(self, request, view):
        if request.user.role == 'support':
            return request.method in ['GET', 'PUT']
        return request.user.role == 'sales'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user == obj.contract_id.customer.sales_contact_id or request.user == obj.contract_id.support_contact_id  # noqa
        else:
            if obj.is_finished is True:
                raise PermissionDenied('You cannot update a finished event')
            if request.user.role == 'support':
                return request.user == obj.contract_id.support_contact_id
            return request.user == obj.contract_id.customer.sales_contact_id
