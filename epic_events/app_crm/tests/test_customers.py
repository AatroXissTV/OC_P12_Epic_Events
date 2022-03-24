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
__version__ = "0.1.22"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from rest_framework.reverse import reverse

# local application imports
from app_users.models import User
from app_crm.models import Customer
from .setup import CustomTestCase

# other imports & constants


class CustomerListTests(CustomTestCase):
    customer_list_url = reverse('app_crm:customers-list')

    # test management
    def test_management_get_customers_list(self):
        """ management get all customers in the db"""
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customer_list_url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(User.objects.all()))

    def test_management_create_prospect(self):
        """ management can create prospect"""
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'prospect',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': False,
        }
        response = test_user.post(self.customer_list_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_management_create_incomplete(self):
        """ check if incomplete data is not accepted"""
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.post(self.customer_list_url, data={'first_name': 'test'}, format='json')  # noqa
        self.assertEqual(response.status_code, 400)

    def test_management_create_customer(self):
        """ management can create customers but sales_contact_id is empty"""
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'prospect',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': True,
        }
        response = test_user.post(self.customer_list_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], None)

    # test sales
    def test_sales_get_customers_list(self):
        """ sales get their own customers and all prospects"""
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customer_list_url, format='json')

        self.assertEqual(response.status_code, 200)
        for item in response.data:
            if item['is_customer'] is True:
                self.assertEqual(item['sales_contact_id'], user.id)
            else:
                self.assertEqual(item['sales_contact_id'], None)

    def test_sales_create_prospect(self):
        """ sales can create prospect"""
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'prospect',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': False,
        }
        response = test_user.post(self.customer_list_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_sales_create_incomplete(self):
        """ check if incomplete data is not accepted"""
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.put('/crm/customers/2/', data={'first_name': 'test'})  # noqa
        self.assertEqual(response.status_code, 400)

    def test_sales_create_customer(self):
        """ sales can create customers sales contact is user.id"""
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'prospect',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': True,
        }
        response = test_user.post(self.customer_list_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], user.id)

    # test support
    def test_support_get_customers_list(self):
        """ support get their own customers"""
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.get(self.customer_list_url, format='json')

        self.assertEqual(response.status_code, 200)
        for item in response.data:
            customer = Customer.objects.get(id=item['id'])
            self.assertIn(customer, Customer.objects.filter(contract__support_contact_id=user.id))  # noqa

    def test_support_create_customers(self):
        """ support are not allowed to create new customers/prospects"""
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'customer',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'is_customer': False
        }
        response = test_user.post(self.customer_list_url, data, format='json')
        self.assertEqual(response.status_code, 403)


class CustomerDetailsTests(CustomTestCase):

    # test management
    def test_management_get_customer_details(self):
        """ management can view any customers in the db """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        id_list = self.get_id_list(Customer.objects.all())

        for i in range(len(id_list)):
            response = test_user.get(reverse('app_crm:customer-detail',
                                             kwargs={'pk': id_list[i]}))
            self.assertEqual(response.status_code, 200)

    def test_management_update_customer(self):
        """ management can update any customers in the db with empty sales_contact_id"""  # noqa
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'customer',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': True,
        }
        response = test_user.put('/crm/customers/3', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], None)

    def test_management_update_customer_to_prospect(self):
        """ management cannot update customer is_customer if true"""
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'updated_email@email.com',
            'is_customer': False
        }
        response = test_user.put('/crm/customers/2/', data)
        self.assertEqual(response.status_code, 400)

        response = test_user.get('/crm/customers/2/')
        self.assertEqual(response.data['is_customer'], True)

    def test_management_update_customer_incomplete(self):
        """ management cannot update customer with incomplete data """
        user = User.objects.get(username='user_management')
        test_user = self.get_token_auth(user)
        response = test_user.put('/crm/customers/2/', data={'first_name': 'test'})  # noqa
        self.assertEqual(response.status_code, 400)

    def test_management_delete_prospect(self):
        """ management can delete prospect """
        user = User.objects.get(username='user_management')
        test_client = self.get_token_auth(user)
        response = test_client.delete(reverse('app_crm:customer-detail', kwargs={'pk': 4}))  # noqa
        self.assertEqual(response.status_code, 204)

    def test_management_delete_customer(self):
        """ management can delete customer """
        user = User.objects.get(username='user_management')
        test_client = self.get_token_auth(user)
        response = test_client.delete(reverse('app_crm:customer-detail', kwargs={'pk': 2}))  # noqa
        self.assertEqual(response.status_code, 204)

    # test sales
    def test_sales_get_customer_details(self):
        """ sales can view customer only of their own """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)

        response = test_user.get('/crm/customers/1/') # noqa
        self.assertEqual(response.status_code, 200)

        response = test_user.get('crm/customers/5/') # noqa
        self.assertEqual(response.status_code, 404)

    def test_sales_update_customer(self):
        """ sales can update customer """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'customer',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': True,
        }
        response = test_user.put('/crm/customers/3/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_customer'], data['is_customer'])
        self.assertEqual(response.data['sales_contact_id'], user.id)

    def test_sales_update_customer_to_prospects(self):
        """ sales cannot update customer to prospect """
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'prsopects',
            'last_name': 'test',
            'email': 'user.customer@gmail.com',
            'phone_number': '+33123456789',
            'mobile': '+33123456789',
            'company_name': 'test',
            'is_customer': False,
        }
        response = test_user.put('/crm/customers/2/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['is_customer'], 'true')
        self.assertEqual(response.data['sales_contact_id'], response.data['sales_contact_id'])  # noqa

    def test_sales_delete_prospect(self):
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.delete(reverse('app_crm:customer-detail', kwargs={'pk': 4})) # noqa
        self.assertEqual(response.status_code, 403)

    def test_sales_delete_customer(self):
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.delete(reverse('app_crm:customer-detail', kwargs={'pk': 2}))  # noqa
        self.assertEqual(response.status_code, 403)

    def test_sales_update_customer_incomplete(self):
        user = User.objects.get(username='user_sales')
        test_user = self.get_token_auth(user)
        response = test_user.put('/crm/customers/2/', data={'first_name': 'test'})  # noqa
        self.assertEqual(response.status_code, 400)

    # test support
    def test_support_get_customer_details(self):
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)

        response = test_user.get('/crm/customers/2/') # noqa
        self.assertEqual(response.status_code, 200)

        response = test_user.get('crm/customers/1/') # noqa
        self.assertEqual(response.status_code, 404)

    def test_support_update_customer(self):
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@gmail.com',
            'is_customer': True
        }
        response = test_user.put('/crm/customers/4/', data)
        self.assertEqual(response.status_code, 404)

    def test_support_delete_customer(self):
        user = User.objects.get(username='user_support')
        test_user = self.get_token_auth(user)
        response = test_user.delete(reverse('app_crm:customer-detail', kwargs={'pk': 4}))  # noqa
        self.assertEqual(response.status_code, 404)
