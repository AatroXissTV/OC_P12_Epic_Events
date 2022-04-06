# app_crm/tests/test_models.py
# created 28/03/2022 at 17:50 by Antoine 'AatroXiss' BEAUDESSON
# last modified 06/04/2022 at 10:48 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/test_models.py:
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

# django imports

# local application imports
from app_crm.models import (
    Customer,
    Contract,
    Event
)
from app_crm.tests.setup import (
    CustomTestCase
)

# other imports & constants


class TestModels(CustomTestCase):
    def test_str_customer(self):
        customer = Customer.objects.get(pk=1)
        self.assertEqual(str(customer), 'John Doe (is customer: True)')
        customer = Customer.objects.get(pk=3)
        self.assertEqual(str(customer), 'Adrien Nougaret (is customer: False)')

    def test_str_contracts(self):
        contract = Contract.objects.get(pk=1)
        self.assertEqual(str(contract), 'Project 1 (is signed: True)')
        contract = Contract.objects.get(pk=2)
        self.assertEqual(str(contract), 'Project 2 (is signed: False)')

    def test_str_event(self):
        event = Event.objects.get(pk=1)
        self.assertEqual(str(event), 'upcoming with support (status: False)')  # noqa
        event = Event.objects.get(pk=2)
        self.assertEqual(str(event), 'upcoming with no support (status: False)')  # noqa