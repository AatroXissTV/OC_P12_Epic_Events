# app_users/models.py
# created 02/03/2022 at 12:27 by Antoine 'AatroXiss' BEAUDESSON
# last modified 02/03/2022 at 12:27 by Antoine 'AatroXiss' BEAUDESSON

""" app_users/models.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.3"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.db import models
from django.contrib.auth.models import AbstractUser

# local application imports

# other imports & constants
ROLE = [
    ('sales', 'sales'),
    ('support', 'support'),
    ('management', 'management'),
]


class User(AbstractUser):
    """
    This class represents the users of the application.
    It uses the AbstractUser class from Django.
    """

    # Fields
    role = models.CharField(max_length=10, choices=ROLE, default='management')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # FKs
