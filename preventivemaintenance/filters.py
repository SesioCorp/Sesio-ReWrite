import django_filters
from django.db.models import Q
from preventivemaintenance.models import *
from asset.models import Asset
from systemandfacility.models import Building, Department, Floor

class PreventiveMaintenanceFilter(django_filters.FilterSet):
    custom_search = django_filters.CharFilter(label="Search", method="custom_filter")
    building = django_filters.ModelChoiceFilter(
        label="Building",
        queryset=Building.objects.all(),
        method="method_building_filter"
    )
    floor = django_filters.ModelChoiceFilter(
        label="Floor", queryset=Floor.objects.all(), method="method_floor_filter"
    )
    department = django_filters.ModelChoiceFilter(
        label="Department",
        queryset=Department.objects.all(),
        method="method_department_filter"
    )
    view = django_filters.ModelChoiceFilter(
        label="View", queryset=Asset.objects.all(), method="method_asset_filter"
    )

    class Meta:
        model = PreventiveMaintenance
        fields = ['slug', 'facility', 'asset', 'status', 'frequency', 'started_at', 'expired_at']
    
    def __init__(self, *args, **kwargs):
        super(PreventiveMaintenanceFilter, self).__init__(*args, **kwargs)
        self.filters['floor'].queryset = Floor.objects.none()
        self.filters['department'].queryset = Department.objects.none()

        if "building" in self.data:
            try:
                building_id = int(self.data.get("building"))
                self.filters['floor'].queryset = Floor.objects.filter(building_id=building_id) 
            except:
                pass
        
        if "floor" in self.data:
            try:
                floor_id = int(self.data.get("floor"))
                self.filters['department'].queryset = Department.objects.filter(floor_id=floor_id)
            except:
                pass

    def method_asset_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(self, queryset, name, value)
        return queryset

    def method_building_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(asset__location__building=value)
        return queryset
    
    def method_floor_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(asset__location__floor=value)
        return queryset

    def method_department_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(asset__location__department=value)
        return queryset

    def custom_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(slug__icontains=value)
                | Q(facility__name__icontains=value)
                | Q(asset__location__building__name__icontains=value)
                | Q(asset__location__floor__number__icontains=value)
                | Q(asset__location__department__name__icontains=value)
            )
        return queryset