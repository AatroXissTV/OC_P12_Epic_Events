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
from rest_framework import status
from rest_framework.reverse import reverse

# local application imports
from app_users.models import User
from app_crm.models import Customer, Contract
from .setup import CustomTestCase

# other imports & constants
CONTRACT_DATA = {}
UPDATE_CONTRACT_DATA = {}


class ContractEndpointTests(CustomTestCase):
    """
    In this class we are testing the contract endpoint
    where only POST and GET requests are allowed.

    Permissions:
        - POST: management, sales
        - GET: management, sales and support
    """
    contract_url = reverse('app_crm:contract-list')

    # POST tests
    def test_management_post_contract(self):
        """
        management role can create a contract for a customer
        - Assert:
            - status code 201
            - contract is created
            - contract support is none
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.contract_url, CONTRACT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), Contract.objects.count()+1)
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_management_post_contract_for_prospects(self):
        """
        management role can't create a contract for a prospect
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.contract_url, CONTRACT_DATA, format='json') # noqa
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sales_post_contract(self):
        """
        sales role can create a contract for a customer
        - Assert:
            - status code 201
            - contract is created
            - contract support is user.id
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.contract_url, CONTRACT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), Contract.objects.count()+1)
        self.assertEqual(response.data['sales_contact_id'], user.id)

    def test_sales_post_contract_for_prospects(self):
        """
        sales role can't create a contract for a prospect
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.contract_url, CONTRACT_DATA, format='json') # noqa
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_post_contract(self):
        """
        support role can't create a contract
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.contract_url, CONTRACT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET tests
    def test_management_get_contracts(self):
        """
        management role can get all contracts
        - Assert:
            - status code 200
            - all contracts are returned
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
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
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for contract in response.data:
            customer = Customer.objects.get(id=contract['customer'])
            self.assertEqual(customer.sales_contact_id, user.id)

    def test_support_get_contracts(self):
        """
        support role can only get contracts
        where they are the support contact id
        - Assert:
            - status code 200
            - item in support contact id is the user
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.contract_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            contract = Contract.objects.get(id=item['id'])
            self.assertIn(contract, Contract.objects.filter(support_contact_id=user.id)) # noqa


class ContractDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the contract details endpoint
    where only GET, PUT requests are allowed.

    Permissions:
        - GET: management, sales and support
        - PUT: management, sales
    """

    # GET tests
    def test_management_get_contract(self):
        """
        management role can get all contracts
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        id_list = self.get_id_list(Contract.objects.all())
        for i in range(len(id_list)):
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': id_list[i]}))
            self.assertEqual(response.status_code, 200)

    def test_sales_get_contract(self):
        """
        sales role can only see contracts
        where they are the sales_contact_id
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        own_customers_ids = self.get_id_list(Customer.objects.filter(sales_contact_id=user.id)) # noqa
        for i in range(len(own_customers_ids)):
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': own_customers_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 200)
        other_ids = self.get_id_list(Contract.objects.exclude(customer__sales_contact_id=user.id)) # noqa
        for i in range(len(other_ids)):
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': other_ids[i]}))
            self.assertEqual(response.status_code, 403)

    def test_support_get_contract(self):
        """
        support role can only see contracts
        where they are the support_contact_id
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        own_contracts_ids = self.get_id_list(Contract.objects.filter(support_contact_id=user.id))  # noqa
        for i in range(len(own_contracts_ids)):
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': own_contracts_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 200)
        other_ids = self.get_id_list(Contract.objects.exclude(support_contact_id=user.id))  # noqa
        for i in range(len(other_ids)):
            response = test_user.get(reverse('app_crm:contract-detail',
                                             kwargs={'pk': other_ids[i]}))
            self.assertEqual(response.status_code, 403)

    # PUT tests
    def test_management_put_contract(self):
        """
        management role can update all contract
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        id_list = self.get_id_list(Contract.objects.all())
        for i in range(len(id_list)):
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': id_list[i]}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 200)

    def test_sales_put_contract(self):
        """
        sales role can only update contracts
        where they are the sales_contact_id
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        own_customers_ids = self.get_id_list(Customer.objects.filter(sales_contact_id=user.id))  # noqa
        for i in range(len(own_customers_ids)):
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': own_customers_ids[i]}),  # noqa
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 200)
        other_ids = self.get_id_list(Contract.objects.exclude(customer__sales_contact_id=user.id))  # noqa
        for i in range(len(other_ids)):
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': other_ids[i]}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 403)

    def test_support_put_contract(self):
        """
        support role can't update contracts
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        id_list = self.get_id_list(Contract.objects.all())
        for i in range(len(id_list)):
            response = test_user.put(reverse('app_crm:contract-detail',
                                             kwargs={'pk': id_list[i]}),
                                     UPDATE_CONTRACT_DATA, format='json')
            self.assertEqual(response.status_code, 403)

    # other methods
    def test_other_methods(self):
        """
        other methods are not allowed on contract details
        - Assert:
            - status code 405
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.delete(reverse('app_crm:contract-detail',
                                            kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) # noqa
