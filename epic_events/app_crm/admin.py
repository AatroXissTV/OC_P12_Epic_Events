# app_crm/admin.py
# created 08/03/2022 at 09:07 by Antoine 'AatroXiss' BEAUDESSON
# last modified 08/03/2022 at 09:07 by Antoine 'AatroXiss' BEAUDESSONx

""" app_crm/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.23"
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
        (
            "Customer/Prospect informations",
            {"fields": ("first_name", "last_name", "email",
                        "phone_number", "mobile", "company_name",
                        "is_customer")}
        ),
        (
            "Sales contact informations",
            {"fields": ("sales_contact_id",)}
        ),
        (
            "Date informations",
            {"fields": ("date_created", "date_updated")}
        )
    )
    read_only_fields = ('date_created', 'date_updated')
    list_display = ('first_name', 'last_name', 'email',
                    'phone_number', 'mobile', 'company_name',
                    'is_customer',)
    list_filter = ('is_customer', 'sales_contact_id',)
    search_fields = ('first_name', 'last_name', 'company_name',
                     'sales_contact_id')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Contract informations",
            {"fields": ("project_name", "amount", "payment_due_date",
                        "is_signed", "customer_id")}
        ),
        (
            "Support contact informations",
            {"fields": ("support_contact_id",)}
        ),
        (
            "Date informations",
            {"fields": ("date_created", "date_updated")}
        )
    )
    read_only_fields = ('date_created', 'date_updated', 'support_contact_id')
    list_display = ('project_name', 'amount', 'payment_due_date',
                    'is_signed', 'customer_id', 'support_contact_id')
    list_filter = ('is_signed', 'customer_id', 'support_contact_id')
    search_fields = ('project_name', 'customer__last_name',
                     'support_contact_id')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Event informations",
            {"fields": ("event_name", "event_date", "attendees",
                        "notes")}
        ),
        (
            "Contract informations",
            {"fields": ("contract_id",)}
        ),
        (
            "Date informations",
            {"fields": ("date_created", "date_updated")}
        ),
    )
    read_only_fields = ('date_created', 'date_updated', 'contract_id')
    list_display = ('event_name', 'event_date', 'attendees',
                    'notes', 'contract_id')
    list_filter = ('contract_id', 'event_name')
    search_fields = ('event_name', 'contract_id')
