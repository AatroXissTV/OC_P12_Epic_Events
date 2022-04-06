# app_crm/tests/test_contracts.py
# created 24/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON
# last modified 06/04/2022 at 12:33 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/test_contracts.py:
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
from rest_framework import status
from rest_framework.reverse import reverse

# local application imports
from app_crm.models import Customer, Contract
from .setup import CustomTestCase

# other imports & constants
CONTRACT_DATA = {
    'project_name': 'Unsigned contract',
    'amount': '100',
    'payment_due_date': '2020-01-01',
    'is_signed': False,
    'customer': 1
}
UPDATE_CONTRACT_DATA = {
    'project_name': 'Signed contract',
    'amount': '100',
    'payment_due_date': '2020-01-01',
    'is_signed': True,
    'customer': 1
}
PROSPECT_CONTRACT_DATA = {
    'project_name': 'Prospect contract',
    'amount': '100',
    'payment_due_date': '2020-01-01',
    'is_signed': False,
    'customer': 3
}


class ContractEndpointTests(CustomTestCase):
    """
    In this class we are testing the contract endpoint
    where only POST and GET requests are allowed.

    Permissions:
    - POST:
        - 'user_management' can't create contracts for customers - 403
        - 'user_management' can't create contracts for prospects - 403
        - 'user_sales' can create contracts for customers - 201
        - 'user_sales' can't create contracts for prospects - 403
        - 'user_support' is not authorized to use post method - 403
    - GET:
        - 'user_management' can get all contracts
        - 'user_sales' can get contracts where they are the sales contact
        - 'user_support' can get contracts where they are the support contact.
    """
    contract_url = reverse('app_crm:contract-list')

    # POST tests
    def test_management_post_contract(self):
        """
        management role can't create a contract for a customer
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.post(self.contract_url, CONTRACT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_management_post_contract_for_prospects(self):
        """
        management role can create a contract for a prospect
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.post(self.contract_url, PROSPECT_CONTRACT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_post_contract(self):
        """
        sales role can create a contract for a customer
        - Assert:
            - status code 201
            - contract support is None
              and will be assigned by management in admin
        """
        test_user = self.get_token_auth("user_sales")
        response = test_user.post(self.contract_url, CONTRACT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['support_contact_id'], None)

    def test_sales_post_contract_for_prospects(self):
        """
        sales role can't create a contract for a prospect
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_sales")
        response = test_user.post(self.contract_url, PROSPECT_CONTRACT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_post_contract(self):
        """
        support role can't create a contract
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_support")
        response = test_user.post(self.contract_url, CONTRACT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET tests
    def test_anon_get_contracts(self):
        """
        unlogged user cannot retrieve contracts
        - Assert:
            - status code 401
        """
        response = self.client.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_management_get_contracts(self):
        """
        management role can get all contracts
        - Assert:
            - status code 200
            - all contracts are returned
        """
        test_user = self.get_token_auth("user_management")
        response = test_user.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contract.objects.count(), len(response.data))

    def test_sales_get_contracts(self):
        """
        sales role can only get contracts
        where the customer sales contact id is the user
        - Assert:
            - status code 200
            - item in sales contact id is the user
        """
        test_user, user = self.get_token_auth_user("user_sales")
        response = test_user.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for contract in response.data:
            customer = Customer.objects.get(id=contract['customer'])
            self.assertEqual(customer.sales_contact_id.id, user.id)

    def test_support_get_contracts(self):
        """
        support role can only get contracts
        where they are the support contact id
        - Assert:
            - status code 200
            - item in support contact id is the user
        """
        test_user, user = self.get_token_auth_user("user_support")
        response = test_user.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            contract = Contract.objects.get(id=item['id'])
            self.assertIn(contract, Contract.objects.filter(
                support_contact_id=user.id))

    # OTHER METHODS
    def test_other_http_methods_contracts(self):
        """
        other http methods are not allowed
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth('user_management')
        for method in ['put', 'patch', 'delete']:
            response = getattr(test_user, method)(self.contract_url)
            self.assertEqual(response.status_code,
                             status.HTTP_403_FORBIDDEN)


class ContractDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the contract details endpoint
    where only GET, PUT requests are allowed.

    Permissions:
    - GET:
        - 'user_management' can get all contracts
        - 'user_sales' can get details
          where customer__sales_contact_id is user.id
        - 'user_support' can get details
          where support_contact_id is user.id
    - PUT:
        - 'user_management' can't update contracts every unsigned contracts
        - 'user_management can't update signed contracts
        - 'user_sales' can update contracts where they are the sales_contact_id
        - 'user_sales can't update signed contracts
        - 'user_support' is not authorized to use PUT method.
    """

    # GET tests
    def test_management_get_contract(self):
        """
        management role can get all contracts
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        test_user = self.get_token_auth("user_management")
        id_list = self.get_id_list(Contract.objects.all())
        for i in id_list:
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sales_get_contract(self):
        """
        sales role can only see contracts
        where they are the sales_contact_id
        - Assert:
            - status code 200
            - for i item status code is 200
            - other items status code is 403
        """
        test_user, user = self.get_token_auth_user("user_sales")

        # GET OWN CONTRACTS
        own_contracts = self.get_id_list(
            Contract.objects.filter(customer__sales_contact_id=user.id))
        for i in own_contracts:
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T GET OTHER CONTRACTS
        other = self.get_id_list(
            Contract.objects.exclude(id__in=own_contracts))
        for i in other:
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_get_contract(self):
        """
        support role can only see contracts
        where they are the support_contact_id
        - Assert:
            - status code 200
            - for i item status code is 200
            - other id status code is 404
        """
        test_user, user = self.get_token_auth_user("user_support")

        # GET OWN CONTRACTS
        own_contracts = self.get_id_list(
            Contract.objects.filter(support_contact_id=user.id))
        for i in own_contracts:
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DON'T GET OTHER CONTRACTS
        other = self.get_id_list(
            Contract.objects.exclude(id__in=own_contracts))
        for i in other:
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PUT tests
    def test_management_put_contract(self):
        """
        management role can't update all contract
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_management")
        id_list = self.get_id_list(Contract.objects.all())
        for i in id_list:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_put_contract_unsigned_to_signed(self):
        """
        sales role can update contracts of their own
        if is_signed is False

        Assert:
            - status code 200 for own events (is_signed=False)
            - status code 403 for other events (is_signed=True)
        """
        test_user, user = self.get_token_auth_user("user_sales")
        unsigned_contracts = self.get_id_list(
            Contract.objects.filter(
                customer__sales_contact_id=user.id,
                is_signed=False))
        for i in unsigned_contracts:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 200)

    def test_sales_put_contract_from_signed_to_unsigned(self):
        """
        sales role can't update contracts
        where they are the sales_contact_id and is signed
        - Assert:
            - for i item status code is 400
        """
        test_user, user = self.get_token_auth_user("user_sales")
        signed_contracts = self.get_id_list(
            Contract.objects.filter(customer__sales_contact_id=user.id,
                                    is_signed=True))
        for i in signed_contracts:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),  # noqa
                                     CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_put_contract_where_not_sales_contact(self):
        """
        sales role can't update contracts
        where they are not the sales_contact_id
        - Assert:
            - for i item status code is 403
        """
        test_user, user = self.get_token_auth_user("user_sales")
        other_contracts = self.get_id_list(
            Contract.objects.exclude(customer__sales_contact_id=user.id))
        for i in other_contracts:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),  # noqa
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 403)

    def test_support_put_contract(self):
        """
        support role can't update contracts
        - Assert:
            - if support_contact_id is user id status code is 403
            - if support_contact_id is not user id status code is 404
        """
        test_user, user = self.get_token_auth_user("user_support")
        own_contracts = self.get_id_list(
            Contract.objects.filter(support_contact_id=user.id))
        for i in own_contracts:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        other_contracts = self.get_id_list(
            Contract.objects.exclude(support_contact_id=user.id))
        for i in other_contracts:
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': i}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
