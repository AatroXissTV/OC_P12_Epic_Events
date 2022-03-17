# app_crm/urls.py
# created 09/03/2022 at 09:55 by Antoine 'AatroXiss' BEAUDESSON
# last modified 17/03/2022 at 16:49 by Antoine 'AatroXiss' BEAUDESSON

""" app_crm/urls.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.12"
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


urlpatterns = [
    path('customers/', views.CustomerList.as_view(), name='customers-list'),
    path('customers/<int:pk>/',
         views.CustomerDetail.as_view(),
         name='customer-detail'),
    path('contracts/', views.ContractList.as_view(), name='contract-list'),
    path('contracts/<int:pk>/',
         views.ContractDetail.as_view(),
         name='contract-detail'),
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/',
         views.EventDetail.as_view(),
         name='event-detail'),
]
