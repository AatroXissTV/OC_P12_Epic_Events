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
__version__ = "0.1.0"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# local application imports
from .models import User

# other imports & constants


admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Personal informations",
         {'fields': ('username', 'password', 'first_name',
                     'last_name', 'email')}),
        ("Permissions",
         {'fields': ('role',)}),
        ("Date informations",
         {'fields': ('date_created', 'date_updated', 'last_login')}),
    )
    readonly_fields = ('date_created', 'date_updated', 'last_login')
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'role')
    list_filter = ('role', 'is_active')
