# app_users/views.py
# created 14/03/2022 at 09:31 by Antoine 'AatroXiss' BEAUDESSON
# last modified 14/03/2022 at 09:31 by Antoine 'AatroXiss' BEAUDESSON

""" app_users/views.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.8"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework_simplejwt.views import TokenViewBase

# django imports

# local application imports
from .serializers import (
    MyTokenObtainSerializer
)

# other imports & constants


class MyTokenObtainView(TokenViewBase):
    serializer_class = MyTokenObtainSerializer
