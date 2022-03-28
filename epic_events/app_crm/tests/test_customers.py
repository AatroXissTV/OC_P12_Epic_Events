# app_crm/tests/customers.py
# created 23/03/2022 at 12:08 by Antoine 'AatroXiss' BEAUDESSON
# last modified 25/03/2022 at 12:41 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/customers.py:
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
    - POST:
        - 'user_management' create a prospect(sales_contact_id=None) - 201
        - 'user_management' create a customer(sales_contact_id=None) - 201
        - 'user_sales' create a prospect(sales_contact_id=None) - 201
        - 'user_sales' create a customer(sales_contact_id=user.id) - 201
        - 'user_support' is not authorized to use POST method - 403
    - GET:
        - 'user_management' can get all prospects/customers - 200
        - 'user_sales' get prospects + customers(sales_contact_id=user.id)-200
        - 'use_support' get customers(contract__support_contact_id=user.id)-200
    - OTHER METHODS:
        - are not allowed for everyone - 405
    """
    customers_url = reverse('app_crm:customers-list')

    # POST tests
    def test_management_post_prospect(self):
        """
        management role can create a new prospect in the DB.
        - Assert:
            - status code 201
            - There is no salesman assigned to it
        """
        test_user = self.get_token_auth('user_management')
        response = test_user.post(self.customers_url, PROSPECT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_management_post_customer(self):
        """
        management can create a new customer in the DB.
        - Assert:
            - status code 201
            - There is no salesman assigned to it
        """
        test_user = self.get_token_auth('user_management')
        response = test_user.post(self.customers_url, CUSTOMER_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_sales_post_prospect(self):
        """
        sales can create a prospect in the db.
        - Assert:
            - status code 201
            - There is no salesman assigned to it
        """
        test_user = self.get_token_auth('user_sales')
        response = test_user.post(self.customers_url, PROSPECT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_sales_post_customer(self):
        """
        sales can create a customer in the db.
        - Assert:
            - status code 201
            - He is assigned to it
        """
        test_user, user = self.get_token_auth_user('user_sales')
        response = test_user.post(self.customers_url, CUSTOMER_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_customer'], CUSTOMER_DATA['is_customer'])  # noqa
        self.assertEqual(response.data['sales_contact_id'], user.id)

    def test_support_post_prospect_and_customer(self):
        """
        support role can't create a prospect or a customer.
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth('user_support')
        response = test_user.post(self.customers_url, PROSPECT_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = test_user.post(self.customers_url, CUSTOMER_DATA,
                                  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET tests
    def test_management_get_customers(self):
        """
        management can see every customers in the DB.
        - Assert:
            - status code 200
            - len of the response is = len User.objects.all()
        """
        test_user = self.get_token_auth('user_management')
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
        test_user, user = self.get_token_auth_user('user_sales')
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
        test_user, user = self.get_token_auth_user("user_support")
        response = test_user.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            customer = Customer.objects.get(id=item['id'])
            self.assertIn(customer, Customer.objects.filter(
                contract__support_contact_id=user.id))

    # OTHERS tests
    def test_other_http_methods(self):
        """
        other http methods are not allowed
        - Assert:
            - status code 405
        """
        test_user = self.get_token_auth('user_management')
        for method in ['put', 'patch', 'delete']:
            response = getattr(test_user, method)(self.customers_url)
            self.assertEqual(response.status_code,
                             status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerDetailEndpointTest(CustomTestCase):
    """
    In this class we are testing the customer endpoint.
    where only GET, PUT and DELETE are allowed.

    Permissions:
        - GET:
            - 'user_management' can get all prospects + customers' - 200
            - 'user_sales' can get details for prospects and customers
               where sales_contact_id == user.id - 200 else 404
            - 'user_support' can get details for customers
              where contract__support_contact_id == user.id - 200 else 404
        - PUT:
            - 'user_management' can update customers and prospects - 200
            - 'user_management can't update customers to prospects - 400
            - 'user_sales' can update prospects and customers
              where sales_contact_id == user.id - 200
            - 'user_sales' can't update customers to prospects
              where sales_contact_id == user.id - 400
            - 'user_support' is not authorized to use this Method - 404
        - DELETE:
            - 'user_management': can delete customers and prospects
            - 'user_sales' not authorized to use this method
            - 'user_support' not authorized to use this method
        - OTHER METHODS:
            - are not allowed for everyone
    """

    # GET tests
    def test_management_get_customer(self):
        """
        management role can retrieve any customer of the DB.
        - Assert:
            - for i item status code is 200
        """
        test_user = self.get_token_auth('user_management')
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
            - if customer is TRUE and sales_contact_id is != user.id then 404
        """
        test_user, user = self.get_token_auth_user('user_sales')

        # GET OWN CUSTOMERS
        own_customers = self.get_id_list(
            Customer.objects.filter(sales_contact_id=user.id))
        for i in range(len(own_customers)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': own_customers[i]}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['sales_contact_id'], user.id)

        # GET PROSPECTS
        prospects = self.get_id_list(
            Customer.objects.filter(is_customer=False))
        for i in range(len(prospects)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospects[i]}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['sales_contact_id'], None)

        # DON'T GET OTHER CUSTOMERS
        other = self.get_id_list(
            Customer.objects.exclude(id__in=own_customers + prospects))
        for i in range(len(other)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': other[i]}))
            self.assertEqual(response.status_code, 404)

    def test_support_get_customer(self):
        """
        sales role can only see their customers
        - Assert:
            - status code 200
            - own customers status code 200 and contract__support_contact_id
            - other customers status code 404
        """
        test_user, user = self.get_token_auth_user('user_support')

        # GET OWN CUSTOMERS
        own_customers = self.get_id_list(
            Customer.objects.filter(contract__support_contact_id=user.id))
        for i in range(len(own_customers)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': own_customers[i]}))
            self.assertEqual(response.status_code, 200)

        # DON'T GET OTHER CUSTOMERS
        other = self.get_id_list(
            Customer.objects.exclude(id__in=own_customers))
        for i in range(len(other)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': other[i]}))
            self.assertEqual(response.status_code, 404)

    # PUT tests
    def test_management_put_prospects_to_customer(self):
        """
        management can update prospects to customers
        - Assert:
            - status code 200
            - sales_contact_id is None
        """
        test_user = self.get_token_auth("user_management")
        prospect = Customer.objects.filter(is_customer=False)
        for i in range(len(prospect)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect[i].id}),
                                     CUSTOMER_DATA, format='json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Customer.objects.get(
                id=prospect[i].id).sales_contact_id,
                None)

    def test_management_put_customer_to_prospect(self):
        """
        management can't update customers to prospect
        - Assert:
            - status code 400
        """
        test_user = self.get_token_auth("user_management")
        customer_ids = self.get_id_list(
            Customer.objects.filter(is_customer=True))
        for i in customer_ids:
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': i}),
                                     PROSPECT_DATA, format='json')
            self.assertEqual(response.status_code, 403)

    def test_sales_put_prospects_to_customer(self):
        """
        sales can update prospects to customers
        - Assert:
            - status code 200
            - sales_contact_id is user.id
        """
        test_user, user = self.get_token_auth_user("user_sales")
        prospect_ids = self.get_id_list(
            Customer.objects.filter(is_customer=False))
        for i in range(len(prospect_ids)):
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': prospect_ids[i]}),
                                     CUSTOMER_DATA, format='json')
            self.assertEqual(response.status_code, 200)
            customer = Customer.objects.get(id=prospect_ids[i])
            self.assertEqual(customer.sales_contact_id.id, user.id)

    def test_sales_put_customer_to_prospect(self):
        """
        sales role can't update customers to prospect
        sales role can't update customers/prospects if
        they are not the sales_contact_id
        - Assert:
            - for it's own customers: status code 403
            - for other customers: status code 404
        """
        test_user, user = self.get_token_auth_user("user_sales")
        own_customers = self.get_id_list(
            Customer.objects.filter(sales_contact_id=user.id,
                                    is_customer=True))
        for i in own_customers:
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': i}),
                                     PROSPECT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        prospects = self.get_id_list(
            Customer.objects.filter(is_customer=False))
        other_customers = self.get_id_list(
            Customer.objects.exclude(id__in=own_customers + prospects))
        for i in other_customers:
            response = test_user.put(reverse('app_crm:customer-detail',
                                             kwargs={'pk': i}),
                                     PROSPECT_DATA, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_support_put_prospects_to_customer(self):
        """
        support can't update prospects to customers
        - Assert:
            - status code 404
        """
        test_user = self.get_token_auth("user_support")
        prospect_ids = self.get_id_list(
            Customer.objects.filter(is_customer=False))
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
        test_user = self.get_token_auth("user_management")
        prospect_ids = self.get_id_list(
            Customer.objects.filter(is_customer=False))
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
        test_user = self.get_token_auth("user_management")
        customer_ids = self.get_id_list(
            Customer.objects.filter(is_customer=True))
        for i in range(len(customer_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': customer_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 204)

    def test_sales_delete_prospect(self):
        """
        sales role can't delete prospects
        - Assert:
            - status code 403
        """
        test_user = self.get_token_auth("user_sales")
        prospect_ids = self.get_id_list(
            Customer.objects.filter(is_customer=False))
        for i in range(len(prospect_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': prospect_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 403)

    def test_sales_delete_customer(self):
        """
        sales can't delete their customers
        - Assert:
            - status code 403
        """
        test_user, user = self.get_token_auth_user("user_sales")
        own_customer_ids = self.get_id_list(
            Customer.objects.filter(sales_contact_id=user.id))
        for i in range(len(own_customer_ids)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': own_customer_ids[i]}))  # noqa
            self.assertEqual(response.status_code, 403)

    def test_support_delete_prospect(self):
        """
        support can't delete their customers
        - Assert:
            - status code 403
        """
        test_user, user = self.get_token_auth_user("user_support")
        own_customers = self.get_id_list(
            Customer.objects.filter(contract__support_contact_id=user.id))
        for i in range(len(own_customers)):
            response = test_user.delete(reverse('app_crm:customer-detail',
                                                kwargs={'pk': own_customers[i]}))  # noqa
            self.assertEqual(response.status_code, 403)
