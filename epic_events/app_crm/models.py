# app_crm/models.py
# created 02/03/2022 at 12:06 by Antoine 'AatroXiss' BEAUDESSON
# last modified 22/03/2022 at 18:17 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/models.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.19"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
)


# local application imports
from app_users.models import User

# other imports & constants


class Customer(models.Model):
    """
    This class represents a customer in the crm.

    Attributes:
        first_name (str): The customer's first name.
        last_name (str): The customer's last name.
        email (str): The customer's email.
        phone_number (str): The customer's phone number.
        mobile (str): The customer's mobile number.
        company_name (str): The customer's company.
        is_customer (bool): Whether the customer is a customer or not.
                            True if the customer is a customer,
                            False otherwise.
    """
    # Fields
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    is_customer = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # FKs
    sales_contact_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    # Methods
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Meta


@receiver(pre_save, sender=Customer)
def check_sales_contact(sender, instance, *args, **kwargs):
    if instance.is_customer is True:
        if instance.sales_contact_id.role == 'sales':
            instance.sales_contact_id = instance.sales_contact_id
        elif instance.sales_contact_id.role == 'management':
            instance.sales_contact_id = None
        else:
            raise ValueError("The user is not a sales contact.")
    else:
        instance.sales_contact_id = None


class Contract(models.Model):
    """
    This class represents a contract in the crm.

    Attributes:
        amount (int): The contract's amount.
        payment_due_date (date): The contract's payment due date.
        is_signed (bool): Whether the contract is signed or not.
                            True if the contract is signed,
                            False otherwise.
    """

    # Fields
    project_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateTimeField()
    is_signed = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # FKs
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='contract',
    )
    support_contact_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    # Methods
    def __str__(self):
        return f"{self.project_name} ({self.is_signed})"

    # Meta


class Event(models.Model):
    """
    This class represents an event in the crm.

    Attributes:
        event_name (str): The event's name.
        event_date (date): The event's date.
        attendees (int): The number of attendees.
        notes (str): The event's notes.
    """

    # Fields
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    attendees = models.IntegerField()
    notes = models.TextField()
    is_finished = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # FKs
    contract_id = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='event',
    )

    # Methods
    def __str__(self):
        return f"{self.event_name} ({self.contract_id})"

    # Meta
