# app_crm/tests/customers.py
# created 23/03/2022 at 12:08 by Antoine 'AatroXiss' BEAUDESSON
# last modified 24/03/2022 at 10:14 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/customers.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.25"
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
from app_crm.models import Customer
from .setup import CustomTestCase

# other imports & constants
CUSTOMER_DATA = {
    'first_name': 'Customer',
    'last_name': 'Test',
    'email': 'user.customer@gmail.com',
    'phone_number': '+33123456789',
    'mobile': '+33123456789',
    'company_name': 'Customer Test',
    'is_customer': True,
}
PROSPECT_DATA = {
    'first_name': 'Prospect',
    'last_name': 'Test',
    'email': 'user.prospect@gmail.com',
    'phone_number': '+33123456789',
    'mobile': '+33123456789',
    'company_name': 'Prospect Test',
    'is_customer': False,
}


class CustomersEndpointTests(CustomTestCase):
    """
    In this class we are testing the customer endpoint.
    where only POST and GET are allowed.

    Permissions:
        - POST: management, sales
        - GET: management, sales, and support
    """
    customers_url = reverse('app_crm:customers-list')

    # POST tests
    def test_management_post_prospect(self):
        """
        management can create a prospect in the db.
        - Assert:
            - status code 201
            - it's a prospect
            - There is no salesman assigned to it
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customers_url, PROSPECT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_customer'], PROSPECT_DATA['is_customer'])  # noqa
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_management_post_customer(self):
        """
        management can create a customer in the db.
        - Assert:
            - status code 201
            - it's a customer
            - There is no salesman assigned to it
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customers_url, CUSTOMER_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_customer'], CUSTOMER_DATA['is_customer'])  # noqa
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_sales_post_prospect(self):
        """
        sales can create a prospect in the db.
        - Assert:
            - status code 201
            - it's a prospect
            - There is no salesman assigned to it
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customers_url, PROSPECT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_customer'], PROSPECT_DATA['is_customer'])  # noqa
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_sales_post_customer(self):
        """
        sales can create a customer in the db.
        - Assert:
            - status code 201
            - it's a customer
            - He is assigned to it
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customers_url, CUSTOMER_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_customer'], CUSTOMER_DATA['is_customer'])  # noqa
        self.assertEqual(response.data['sales_contact_id'], user.id)

    def test_support_post_prospect_and_customer(self):
        """
        support role can't create a prospect or a customer.
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customers_url, PROSPECT_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = test_user.post(self.customers_url, CUSTOMER_DATA, format='json')  # noqa
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET tests
    def test_management_get_customers(self):
        """
        management can see every customers in the DB.
        - Assert:
            - status code 200
            - len of the response is = len User.objects.all()
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customer.objects.count())

    def test_sales_get_customers(self):
        """
        sales role can only see their customers + all the prospects
        - Assert:
            - status code 200
            - if is_customer then sales_contact_id = user.id
            - if is_customer is False then sales_contact_id = None
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            if item['is_customer'] is True:
                self.assertEqual(item['sales_contact_id'], user.id)
            else:
                self.assertEqual(item['sales_contact_id'], None)

    def test_support_get_customers(self):
        """
        support role can only see their own customers
        - Assert:
            - status code 200
            - customer__contract__support_contact_id is user.id
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            customer = Customer.objects.get(id=item['id'])
            self.assertIn(customer, Customer.objects.filter(contract__support_contact_id=user.id))  # noqa

    # OTHERS tests
    def test_other_http_methods(self):
        """
        other http methods are not allowed
        - Assert:
            - status code 405
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.put(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # noqa
        response = test_user.patch(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # noqa
        response = test_user.delete(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # noqa


class CustomerDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the customer endpoint.
    where only GET, PUT and DELETE are allowed.

    Permissions:
        - GET: management, sales, and support
        - PUT: management, sales
        - DELETE: management
    """

    # GET tests
    def test_management_get_customer(self):
        """
        management role can retrieve any customer of the DB.
        - Assert:
            - status code 200
            - for i item status code is 200
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        id_list = self.get_id_list(Customer.objects.all())

        for i in range(len(id_list)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': id_list[i]}))
            self.assertEqual(response.status_code, 200)

    def test_sales_get_customer(self):
        """
        sales role can only see their customers + all the prospects
        - Assert:
            - status code 200
            - if is_customer then sales_contact_id = user.id
            - if is_customer is False then sales_contact_id = None
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        own_customers_ids = self.get_id_list(Customer.objects.filter(sales_contact_id=user.id))  # noqa
        for i in range(len(own_customers_ids)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': own_customers_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 200)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect_ids[i]}))
            self.assertEqual(response.status_code, 200)
        other_ids = self.get_id_list(Customer.objects.exclude(id__in=own_customers_ids + prospect_ids))  # noqa
        for i in range(len(other_ids)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': other_ids[i]}))
            self.assertEqual(response.status_code, 404)

    def test_support_get_customer(self):
        """
        sales role can only see their customers
        - Assert:
            - status code 200
            - own customers status code 200
            - other customers status code 403
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        own_customers_ids = self.get_id_list(Customer.objects.filter(contract__support_contact_id=user.id))  # noqa
        for i in range(len(own_customers_ids)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': own_customers_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 200)
        other_ids = self.get_id_list(Customer.objects.exclude(id__in=own_customers_ids))  # noqa
        for i in range(len(other_ids)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': other_ids[i]}))
            self.assertEqual(response.status_code, 404)

    # PUT tests
    def test_management_put_prospects_to_customer(self):
        """
        management can update prospects to customers
        - Assert:
            - status code 200
            - sales_contact_id is None
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect_ids[i]}),
                                     CUSTOMER_DATA, format='json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Customer.objects.get(id=prospect_ids[i]).sales_contact_id, None)  # noqa

    def test_management_put_customer_to_prospect(self):
        """
        management can't update customers to prospect
        - Assert:
            - status code 400
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        customer_ids = self.get_id_list(Customer.objects.filter(is_customer=True))  # noqa
        for i in range(len(customer_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': customer_ids[i]}),
                                     PROSPECT_DATA, format='json')
            self.assertEqual(response.status_code, 400)

    def test_sales_put_prospects_to_customer(self):
        """
        sales can update prospects to customers
        - Assert:
            - status code 200
            - sales_contact_id is user.id
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect_ids[i]}),
                                     CUSTOMER_DATA, format='json')
            self.assertEqual(response.status_code, 200)
            customer = Customer.objects.get(id=prospect_ids[i])
            self.assertEqual(customer.sales_contact_id.id, user.id)  # noqa

    def test_sales_put_customer_to_prospect(self):
        """
        sales can't update customers to prospect
        - Assert:
            - status code 400
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        customer_ids = self.get_id_list(Customer.objects.filter(is_customer=True))  # noqa
        for i in range(len(customer_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': customer_ids[i]}),
                                     PROSPECT_DATA, format='json')
            self.assertEqual(response.status_code, 400)

    def test_support_put_prospects_to_customer(self):
        """
        support can't update prospects to customers
        - Assert:
            - status code 404
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect_ids[i]}),
                                     CUSTOMER_DATA, format='json')
            self.assertEqual(response.status_code, 404)

    # DELETE tests
    def test_management_delete_prospect(self):
        """
        management can delete prospects
        - Assert:
            - status code 204
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': prospect_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 204)

    def test_management_delete_customer(self):
        """
        management can delete customers
        - Assert:
            - status code 204
        """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        customer_ids = self.get_id_list(Customer.objects.filter(is_customer=True))  # noqa
        for i in range(len(customer_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': customer_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 204)

    def test_sales_delete_prospect(self):
        """
        sales role can delete prospects
        - Assert:
            - status code 403
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': prospect_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 403)

    def test_sales_delete_customer(self):
        """
        sales can't delete customers
        - Assert:
            - status code 404
        """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        customer_ids = self.get_id_list(Customer.objects.filter(is_customer=True))  # noqa
        for i in range(len(customer_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': customer_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 404)

    def test_support_delete_prsopect(self):
        """
        support can't delete prospects
        - Assert:
            - status code 404
        """
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        prospect_ids = self.get_id_list(Customer.objects.filter(is_customer=False))  # noqa
        for i in range(len(prospect_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': prospect_ids[i]}))  # noqa 
            self.assertEqual(response.status_code, 404)
