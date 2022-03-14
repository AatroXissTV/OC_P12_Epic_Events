# app_users/serializers.py
# created 14/03/2022 at 09:24 by Antoine 'AatroXiss' BEAUDESSON
# last modified 14/03/2022 at 09:24 by Antoine 'AatroXiss' BEAUDESSON

""" app_users/serializers.py:
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

# django imports
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
)
from rest_framework_simplejwt.tokens import AccessToken

# local application imports

# other imports & constants


class MyTokenObtainSerializer(TokenObtainSerializer):
    """
    Custom token obtain serializer.
    """

    @classmethod
    def get_token(cls, user):
        """
        Returns a token for a given user.
        """
        return AccessToken.for_user(user)

    def validated(self, attrs):
        data = super().validated(attrs)
        access = self.get_token(self.user)
        data['access'] = str(access)
