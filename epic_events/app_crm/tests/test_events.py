# app_crm/tests/test_contracts.py
# created 24/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 28/03/2022 at 12:10 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/test_contracts.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.0"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from rest_framework import status
from rest_framework.reverse import reverse

# local application imports
from app_crm.models import (
    Event
)
from .setup import CustomTestCase

# other imports & constants
EVENT_DATA = {
    'event_name': 'Unfinished Event',
    'event_date': '2023-03-23T11:38:00.000Z',
    'attendees': "100",
    'notes': 'This is a test event',
    'is_finished': False,
    'contract_id': 1,
}

UNSIGNED_EVENT_DATA = {
    'event_name': 'Unfinished Event',
    'event_date': '2023-03-23T11:38:00.000Z',
    'attendees': "100",
    'notes': 'This is a test event',
    'is_finished': False,
    'contract_id': 2,
}

FINISHED_EVENT_DATA = {
    'event_name': 'Finished Event',
    'event_date': '2023-03-23T11:38:00.000Z',
    'attendees': "100",
    'notes': 'This is a test event',
    'is_finished': True,
    'contract_id': 1,
}


class EventEndpointTests(CustomTestCase):
    """
    In this class we are testing the event endpoint
    where only POST and GET requests are allowed.

    Permissions:
    - POST:
        - 'user_management' can create an event for a signed contract
        - 'user_management' can't create an event for an unsigned contract
        - 'user_sales' can create an event for a signed contract
        where he is the sales_contact
        - 'user_sales' can't create an event for an unsigned contract
        - 'user_support can create an event for a signed contracts
        where he is the support_contact
        - 'user_support' can't create an event for an unsigned contract
    - GET:
        - 'user_management' can get all events
        - 'user_sales' can get events
          where the contract_id__customer__sales_contact_id is user
        - 'user_support' can get events
          where the contract_id__support_contact_id is user
    """
    event_url = reverse('app_crm:event-list')

    # POST tests
    def test_management_post_event(self):
        """
        management roles can post new events on signed contracts
        - Assert:
            - status code 201
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_management_post_event_with_unsigned_contract(self):
        """
        management role cannot create a new event if the contract isn't signed
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.post(self.event_url, UNSIGNED_EVENT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_post_event(self):
        """
        sales role can create a new event on signed contracts
        - Assert:
            - status code 201
            - response data is correct
        """
        test_user = self.get_token_auth("user_sales")
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sales_post_event_with_unsigned_contract(self):
        """
        sales role cannot create a new event if the contract isn't signed
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_sales")
        response = test_user.post(self.event_url, UNSIGNED_EVENT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_post_event(self):
        """
        support role can create a new evetn if the contract is signed
        - Assert:
            - status code 201
        """
        test_user = self.get_token_auth("user_support")
        response = test_user.post(self.event_url, EVENT_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_support_post_event_with_unsigned_contract(self):
        """
        support role cannot create a new event if the contract isn't signed
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_support")
        response = test_user.post(self.event_url, UNSIGNED_EVENT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET tests
    def test_management_get_event(self):
        """"
        management role can get every events in the db
        - Assert:
            - status code 200
            - all events are returned
        """
        test_user = self.get_token_auth("user_management")
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
        test_user, user = self.get_token_auth_user("user_sales")
        own_events = Event.objects.filter(
            contract_id__customer__sales_contact_id=user.id)
        response = test_user.get(self.event_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(own_events))

    def test_support_get_event(self):
        """
        support role can only get events
        where they are assigned as support contact
        - Assert:
            - status code 200
            - response data is correct
        """
        test_user, user = self.get_token_auth_user("user_support")
        response = test_user.get(self.event_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertEqual(
                Event.objects.get(
                    contract_id=item['contract_id']).contract_id.support_contact_id.id, user.id)  # noqa: E501

    def other_http_methods_events(self):
        """
        other http methods are not allowed
        - Assert:
            - status code 405
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.get(self.event_url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class EventDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the event details endpoint
    where only GET, PUT requests are allowed.

    Permissions:
    - GET:
        - 'user_management' can get all events
        - 'user_sales' can get details on events
          where contract_id__customer__sales_contact_id is user
        - 'user_support' can get details on events where
          contract_id__support_contact_id is user
    - PUT:
        - 'user_management' can update unfinished event
        - 'user_management' can't update finished events
        - 'user_sales' can update unfinished event
        - 'user_sales' can't update finished event
        - 'user_support' can update unfinished event
        - 'user_support' can't update finished event
    - DELETE:
        - 'user_management' can delete unfinished event
        - 'user_management' can't delete finished event
        - 'user_sales' can't delete event
        - 'user_support can't delete event
    """

    # GET tests
    def test_management_get_event_detail(self):
        """
        management role can get all events
        - Assert:
            - status code 200
            - for i item status code 200
        """
        test_user = self.get_token_auth("user_management")
        id_list = self.get_id_list(Event.objects.all())
        for i in id_list:
            response = test_user.get(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}))  # noqa
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sales_get_event_detail(self):
        """
        sales role can only get events
        where contract_id__contract__sales_contact == user.id
        - Assert:
            - status code 200
            - for i item status code 200
            - other 404
        """
        test_user, user = self.get_token_auth_user("user_sales")

        # GET OWN EVENTS
        own_event = self.get_id_list(
            Event.objects.filter(
                contract_id__customer__sales_contact_id=user.id))
        for i in own_event:
            response = test_user.get(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T GET OTHER EVENTS
        other = self.get_id_list(
            Event.objects.exclude(
                id__in=own_event))
        for i in other:
            response = test_user.get(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_support_get_event_detail(self):
        """
        support role can only get events
        where they are assigned as support contact
        - Assert:
            - status code 200
            - for i item status code 200
        """
        test_user, user = self.get_token_auth_user("user_support")

        # OWN EVENTS
        own_event = self.get_id_list(
            Event.objects.filter(
                contract_id__support_contact_id=user.id))
        for i in own_event:
            response = test_user.get(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T GET OTHER EVENTS
        other = self.get_id_list(
            Event.objects.exclude(
                id__in=own_event))
        for i in other:
            response = test_user.get(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PUT tests
    def test_management_put_event_detail(self):
        """
        management role can only update events
        where status is not finished
        - Assert:
            - status code 200
        """
        test_user, user = self.get_token_auth_user("user_management")
        unfinished_event = self.get_id_list(
            Event.objects.filter(
                is_finished=False))
        for i in unfinished_event:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}),
                                     data=FINISHED_EVENT_DATA,
                                     format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T UPDATE FINISHED EVENTS
        finished_event = self.get_id_list(
            Event.objects.filter(
                is_finished=True))
        for i in finished_event:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}),
                                     data=EVENT_DATA,
                                     format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_put_event_detail(self):
        """
        sales role can only update events
        where they are assigned as sales_contact
        - Assert:
            - status code 200
        """
        test_user, user = self.get_token_auth_user("user_sales")
        own_event = self.get_id_list(
            Event.objects.filter(
                contract_id__customer__sales_contact_id=user.id))
        for i in own_event:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}),
                                     data=FINISHED_EVENT_DATA,
                                     format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        other = self.get_id_list(
            Event.objects.exclude(
                id__in=own_event))
        for i in other:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}),
                                     data=EVENT_DATA,
                                     format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_put_event_detail(self):
        """
        support role can only update events
        where they are assigned as support contact
        - Assert:
            - status code 200
            - response data is correct
        """
        test_user, user = self.get_token_auth_user("user_support")

        # PUT OWN UNFINISHED EVENTS
        own_event = self.get_id_list(
            Event.objects.filter(
                contract_id__support_contact_id=user.id,
                is_finished=False))
        for id in own_event:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': id}),
                                     FINISHED_EVENT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T PUT OTHER EVENTS
        other = self.get_id_list(
            Event.objects.exclude(
                id__in=own_event))
        for i in other:
            response = test_user.put(reverse('app_crm:event-detail',
                                             kwargs={'pk': i}),
                                     FINISHED_EVENT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE tests
    def test_management_delete_event_detail(self):
        """
        management can delete event if it is not finished
        - Assert:
            - status code 204
        """
        test_user = self.get_token_auth("user_management")
        id_list = self.get_id_list(Event.objects.filter(is_finished=False))  # noqa
        for i in id_list:
            response = test_user.delete(reverse('app_crm:event-detail',
                                                kwargs={'pk': i}))
            self.assertEqual(response.status_code, 204)

    def test_management_delete_event_where_event_is_finished(self):
        """
        management role can't delete event if contract is_signed = True
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_management")
        id_list = self.get_id_list(Event.objects.filter(is_finished=True))  # noqa
        for id in range(len(id_list)):
            response = test_user.delete(reverse('app_crm:event-detail',
                                                kwargs={'pk': id_list[id]}))
            self.assertEqual(response.status_code, 403)

    def test_sales_delete_event_detail(self):
        """
        sales role can't delete events
        - Assert:
            - status code 403
        """
        test_user, user = self.get_token_auth_user("user_sales")
        id_list = self.get_id_list(
            Event.objects.filter(
                contract_id__customer__sales_contact_id=user.id))
        for id in range(len(id_list)):
            response = test_user.delete(reverse('app_crm:event-detail',
                                                kwargs={'pk': id_list[id]}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_delete_event_detail(self):
        """
        support role can't delete events
        - Assert:
            - status code 403
        """
        test_user, user = self.get_token_auth_user("user_support")
        id_list = self.get_id_list(
            Event.objects.filter(
                contract_id__support_contact_id=user.id))
        for id in range(len(id_list)):
            response = test_user.delete(reverse('app_crm:event-detail',
                                                kwargs={'pk': id_list[id]}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
