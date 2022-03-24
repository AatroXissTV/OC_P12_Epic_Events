# app_crm/tests/test_contracts.py
# created 24/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 24/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/test_contracts.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.24"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports

# local application imports
from .setup import CustomTestCase

# other imports & constants
CONTRACT_DATA = {}
UPDATE_CONTRACT_DATA = {}


class EventEndpointTests(CustomTestCase):
    """
    In this class we are testing the event endpoint
    where only POST and GET requests are allowed.

    Permissions:
        - POST: management, sales
        - GET: management, sales and support
    """
    pass


class EventDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the event details endpoint
    where only GET, PUT requests are allowed.

    Permissions:
        - GET: management, sales and support
        - PUT: management, sales
        - DELETE: management, sales
    """
    pass
