import django_filters
from systemandfacility.models import Building, Department, Floor
from workorder.models import WorkOrder
from django.db.models import Q


class WorkOrderFilter(django_filters.FilterSet):
    building = django_filters.ModelChoiceFilter(
        label = "Building",
        queryset = Building.objects.all(),
        method = "building_filter"
    )
    
    floor = django_filters.ModelChoiceFilter(
        label = "Floor",
        queryset = Floor.objects.all(),
        method = "floor_filter"
    )

    department = django_filters.ModelChoiceFilter(
        label = "Department",
        queryset = Department.objects.all(),
        method = "department_filter"
    )

    custom_search = django_filters.CharFilter(
        label = "Custom Search",
        method = "custom_search_filter"
    )

    class Meta:
        model = WorkOrder
        fields = ["building", "floor", "department", "custom_search"]

    def building_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(location__building=value)
        return queryset

    def floor_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(location__floor=value)
        return queryset

    def department_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(location__department=value)
        return queryset

    def custom_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(facility__name__icontains=value)
                |Q(asset__slug__icontains=value)
                |Q(location__specific_location__icontains=value)
                |Q(location__building__name__icontains=value)
                |Q(location__department__name__icontains=value)
                |Q(location__floor__number__icontains=value)
            )
        return queryset
