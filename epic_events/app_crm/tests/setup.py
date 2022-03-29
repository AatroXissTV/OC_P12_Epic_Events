# app_crm/tests/setup.py
# created 23/03/2022 at 11:19 by Antoine 'AatroXiss' BEAUDESSON
# last modified 24/03/2022 at 10:14 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/tests/setup.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.23"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# local application imports
from app_users.models import User

# other imports & constants
PASSWORD = "BgfpBe4qS8$Gy76$G#LfEbKxxxMY"
LOGIN_URL = reverse('app_users:login')


class CustomTestCase(APITestCase):

    def setUp(self):
        """
        Create test users.
        and load initial data
        """
        User.objects.create_user(
            id=1,
            username='user_management',
            password=PASSWORD,
            email='user.management@epicevents.com',
            role='management',
            first_name='User',
            last_name='Management',)
        User.objects.create_user(
            id=2,
            username='user_sales',
            password=PASSWORD,
            email='user.sales@epicevents.com',
            role='sales',
            first_name='User',
            last_name='Sales',)
        User.objects.create_user(
            id=3,
            username='user_support',
            password=PASSWORD,
            email='user.support@epicevents.com',
            role='support',
            first_name='User',
            last_name='Support',)
        call_command('loaddata', 'app_crm/fixtures/initial_data.json')

    def get_token_auth(self, username):
        user = User.objects.get(username=username)
        data = {
            'username': user.username,
            'password': PASSWORD,
        }
        response = self.client.post(LOGIN_URL, data, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return self.client

    def get_token_auth_user(self, username):
        user = User.objects.get(username=username)
        data = {
            'username': user.username,
            'password': PASSWORD,
        }
        response = self.client.post(LOGIN_URL, data, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return self.client, user

    @staticmethod
    def get_id_list(queryset):
        """ Returns list of available ids in current queryset"""
        id_list = []
        for i in range(len(queryset)):
            id_list.append(queryset[i].id)
        return id_list
