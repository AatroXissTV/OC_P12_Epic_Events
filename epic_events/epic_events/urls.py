# epic_events/urls.py
# created 07/03/2022 at 15:47 by Antoine 'AatroXiss' BEAUDESSON
# last modified 07/03/2022 at 15:47 by Antoine 'AatroXiss' BEAUDESSON

"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.18"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from rest_framework_nested import routers

# django imports
from django.contrib import admin
from django.urls import path, include

# local application imports
from app_crm import views

# other imports & constants

router = routers.SimpleRouter()
router.register('customer', views.CustomerViewSet)

customer_router = routers.NestedSimpleRouter(
    router,
    'customer',
    lookup='customer'
)
customer_router.register(
    'contract',
    views.ContractViewSet,
    basename='customer-contract'
)
contract_router = routers.NestedSimpleRouter(
    customer_router,
    'contract',
    lookup='contract'
)
contract_router.register(
    'event',
    views.EventViewSet,
    basename='contract-event'
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/', include(customer_router.urls)),
    path('api/', include(contract_router.urls)),
]
