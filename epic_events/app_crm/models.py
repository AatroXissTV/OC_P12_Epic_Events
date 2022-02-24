# models.py
# created 22/02/2022 at 10:23 by Antoine 'AatroXiss' BEAUDESSON
# last modified 24/02/2022 at 10:18 by Antoine 'AatroXiss' BEAUDESSON

""" models.py

To do:
    - Add the models
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2020, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = "MIT"
__version__ = "0.0.4"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# Django imports
from django.db import models

# standard library imports

# third party imports

# local imports

# other imports

# constants


class Customer(models.Model):
    """
    This class represents a customer in the CRM.
    A prospect is immediately considered as a customer.
    However, he truly becomes a customer when the field
    'is_customer' is set to True.
    By default the newly added person is a prospect (is_customer=False).

    Attributes:
    :arg first_name: The first name of the customer.
    :arg last_name: The last name of the customer.
    :arg email: The email of the customer.
    :arg phone_number: The phone number of the customer.
    :arg mobile: The mobile phone number of the customer.
    :arg company_name: The company name of the customer.
    :arg is_customer: A boolean indicating if the customer is a customer.
    """

    customer_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    is_customer = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    """
    This class represents a contract in the CRM.

    Attributes:
    :arg project_name: The name of the project.
    :arg is_signed: A boolean indicating if the contract is signed.
    :arg amount: The amount of the contract.
    :arg payment_due_date: The payment due date of the contract.
    """

    contract_id = models.AutoField(primary_key=True)

    project_name = models.CharField(max_length=100)
    is_signed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Foreign keys
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Event(models.Model):
    pass
