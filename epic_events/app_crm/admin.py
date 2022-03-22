# app_crm/admin.py
# created 08/03/2022 at 09:07 by Antoine 'AatroXiss' BEAUDESSON
# last modified 22/03/2022 at 10:39 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/admin.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.18"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.contrib import admin

# local application imports
from .models import (
    Customer,
    Contract,
    Event
)

# other imports & constants


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Prospect/Customer informations",
         {'fields': ('first_name', 'last_name', 'email',
                     'phone_number', 'mobile')}),
        ("Sales contact informations",
         {'fields': ('sales_contact_id', 'is_customer')}),
        ("Date informations",
         {'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('full_name', 'company_name', 'email', 'phone_number',
                    'mobile', 'is_customer', 'sales_contact_name')
    list_filter = ('is_customer', 'sales_contact_id')
    search_fields = ('first_name', 'last_name', 'company_name',
                     'sales_contact_id__first_name',
                     'sales_contact_id__last_name',
                     'sales_contact_id')

    @staticmethod
    def full_name(obj):
        last_name = obj.last_name.upper()
        return f"{obj.first_name} {last_name}"

    @staticmethod
    def sales_contact_name(obj):
        if obj.sales_contact_id is None:
            return "-"
        first_name = obj.sales_contact_id.first_name
        last_name = obj.sales_contact_id.last_name.upper()
        contact_id = obj.sales_contact_id.id
        return f"{first_name} {last_name} (id:{contact_id})"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contract informations",
         {'fields': ('customer', 'amount', 'payment_due_date')}),
        ("Support informations",
         {'fields': ('support_contact_id', 'is_signed')}),
        ("Date informations",
         {'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('contract_number', 'support_contact_id',
                    'support_contact_name', 'customer',
                    'amount', 'payment_due_date', 'is_signed')
    list_filter = ('is_signed', 'support_contact_id')
    search_fields = ('contract_number', 'customer__last_name')

    @staticmethod
    def contract_number(obj):
        return f"Contract #{obj.id}"

    @staticmethod
    def support_contact_name(obj):
        if obj.support_contact_id is None:
            return "No support contact"
        else:
            first_name = obj.support_contact_id.first_name
            last_name = obj.support_contact_id.last_name.upper()
            contact_id = obj.support_contact_id.id
            return f"{first_name} {last_name} (id:{contact_id})"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Event informations",
         {'fields': ('event_name', 'event_date', 'attendees')}),
        ("Contract informations",
         {'fields': ('contract_id',)}),
        ("Support informations",
            {'fields': ('notes',)}),
        ("Date informations",
            {'fields': ('date_created', 'date_updated')}),
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('event_name', 'event_date',
                    'contract_id', 'support_contact_id',
                    'attendees', 'notes')
    list_filter = ('contract_id',)
    search_filters = ('event_name', 'contract_id', 'customer_last_name')

    @staticmethod
    def support_contact_id(obj):
        if obj.contract_id.support_contact_id.id is not None:
            return obj.contract_id.support_contact_id.id
        else:
            return "No support contact"

    @staticmethod
    def customer_last_name(obj):
        return obj.contract.customer.last_name
