# app_users/admin.py
# created 02/03/2022 at 12:54 by Antoine 'AatroXiss' BEAUDESSON
# last modified 02/03/2022 at 12:54 by Antoine 'AatroXiss' BEAUDESSON

""" app_users/admin.py:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.4"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.contrib import admin

# local application imports
from .models import User

# other imports & constants


admin.site.register(User)
