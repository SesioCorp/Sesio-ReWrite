import django_filters
from preventivemaintenance.models import *

class PreventiveMaintenanceFilter(django_filters.FilterSet):
    class Meta:
        model = PreventiveMaintenance
        fields = ['slug', 'facility', 'asset', 'status', 'frequency', 'started_at', 'expired_at']
    