# app_users/urls.py
# created 09/03/2022 at 09:58 by Antoine 'AatroXiss' BEAUDESSON
# last modified 09/03/2022 at 10:22 by Antoine 'AatroXiss' BEAUDESSON

""" app_users/urls.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.2"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

# local application imports

# other imports & constants


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
