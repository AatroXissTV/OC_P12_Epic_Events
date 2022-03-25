# app_crm/tests/test_contracts.py
# created 24/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 25/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/test_contracts.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.26"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from rest_framework import status
from rest_framework.reverse import reverse

# local application imports
from app_users.models import (
    User,
)
from app_crm.models import (
    Event
)
from .setup import CustomTestCase

# other imports & constants
EVENT_DATA = {}
UNSIGNED_EVENT_DATA = {}


class EventEndpointTests(CustomTestCase):
    """
    In this class we are testing the event endpoint
    where only POST and GET requests are allowed.

    Permissions:
        - POST: management, sales, support
        - GET: management, sales and support
    """
    event_url = reverse('app_crm:event-list')

    # POST tests
    def test_management_post_event(self):
        """
        management roles can post new events on signed contracts
        - Assert:
            - status code 201
            - response data is correct
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contract_id'], EVENT_DATA['contract_id'])  # noqa: E501

    def test_management_post_event_with_unsigned_contract(self):
        """
        management role cannot create a new event if the contract isn't signed
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.event_url, UNSIGNED_EVENT_DATA, format='json')  # noqa: E501
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_post_event(self):
        """
        sales role can create a new event on signed contracts
        - Assert:
            - status code 201
            - response data is correct
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contract_id'], EVENT_DATA['contract_id'])  # noqa: E501

    def test_sales_post_event_with_unsigned_contract(self):
        """
        sales role cannot create a new event if the contract isn't signed
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.event_url, UNSIGNED_EVENT_DATA, format='json')  # noqa: E501
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_post_event(self):
        """
        support role can create a new evetn if the contract is signed
        - Assert:
            - status code 201
            - response data is correct
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contract_id'], EVENT_DATA['contract_id'])  # noqa: E501

    # GET tests
    def test_management_get_event(self):
        """"
        management role can get every events in the db
        - Assert:
            - status code 200
            - response data is correct
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.event_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), len(response.data))

    def test_sales_get_event(self):
        """
        sales role can only get events
        where contract_id__contract__sales_contact == user.id
        - Assert:
            - status code 200
            - response data is correct
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.event_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertEqual(Event.objects.get(contract_id=item['contract_id']).contract_id.contract.sales_contact_id, user)  # noqa: E501

    def test_support_get_event(self):
        """
        support role can only get events
        where they are assigned as support contact
        - Assert:
            - status code 200
            - response data is correct
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.event_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertEqual(Event.objects.get(contract_id=item['contract_id']).contract_id.support_contact_id, user)  # noqa: E501


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
