# app_crm/permissions.py
# created 18/03/2022 at 15:05 by Antoine 'AatroXiss' BEAUDESSON
# last modified 21/03/2022 at 10:38 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/permissions.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.15"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

# django imports

# local application imports
from .models import (
    Customer,
    Contract,
)

# other imports & constants


class CustomerPermissions(permissions.BasePermission):
    """
    This class handles permissions for the Customer endpoints

    management: all permissions are granted
    sales: can CREATE new customers and prospects
           can VIEW and UPDATE any prospects and customers of their own
           can DELETE prospects only
    support: can VIEW their own customers
    """

    def has_permission(self, request, view):
        if request.user.role == "management":
            return True

        try:
            customer = get_object_or_404(Customer, pk=view.kwargs['pk'])
            if request.method == 'DELETE':
                return request.user.role == 'sales' and customer.is_customer is False  # noqa
            elif request.user.role == 'sales':
                return request.user == customer.sales_contact_id or customer.is_customer is False  # noqa
            elif request.user.role == 'support' and request.method in permissions.SAFE_METHODS:  # noqa
                return customer in Customer.objects.filter(contract__event__support_contact_id=request.user)  # noqa

        except KeyError:
            if request.user.role == 'support':
                return request.method in permissions.SAFE_METHODS
            return request.user.role == 'sales'


class ContractPermissions(permissions.BasePermission):
    """
    This class handles permissions for the Contract endpoints

    management: all permissions are granted
    sales: can CREATE new contracts
           can VIEW and UPDATE any contracts of their own if not signed
    support: can VIEW their own contracts
    """

    def has_permission(self, request, view):
        if request.user.role == 'management':
            return True

        try:
            contract = get_object_or_404(Contract, pk=view.kwargs['pk'])
            if request.method in permissions.SAFE_METHODS:
                if request.user.role == 'support':
                    return request.user == contract.event.support_contact_id
                elif request.user.role == 'sales':
                    return request.user == contract.sales_contact_id
            return request.user == contract.sales_contact_id and contract.is_signed is False  # noqa

        except KeyError:
            if request.user.role == 'support':
                return request.method in permissions.SAFE_METHODS
            return request.user.role == 'sales'
