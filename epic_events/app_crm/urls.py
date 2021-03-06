# app_crm/urls.py
# created 09/03/2022 at 09:55 by Antoine 'AatroXiss' BEAUDESSON
# last modified 23/03/2022 at 14:36 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/urls.py:
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
from django.urls import path

# local application imports
from . import views

# other imports & constants

app_name = 'app_crm'
urlpatterns = [
    path('customers/',
         views.CustomerViewSet.as_view({'get': 'list',
                                        'post': 'create'}),
         name='customers-list'),
    path('customers/<int:pk>/',
         views.CustomerViewSet.as_view({'get': 'retrieve',
                                        'put': 'update',
                                        'delete': 'destroy'}),
         name='customer-detail'),
    path('contracts/',
         views.ContractViewSet.as_view({'get': 'list',
                                        'post': 'create'}),
         name='contract-list'),
    path('contracts/<int:pk>/',
         views.ContractViewSet.as_view({'get': 'retrieve',
                                        'put': 'update'}),
         name='contract-detail'),
    path('events/',
         views.EventViewSet.as_view({'get': 'list',
                                     'post': 'create'}),
         name='event-list'),
    path('events/<int:pk>/',
         views.EventViewSet.as_view({'get': 'retrieve',
                                     'put': 'update',
                                     'delete': 'destroy'}),
         name='event-detail'),
]
