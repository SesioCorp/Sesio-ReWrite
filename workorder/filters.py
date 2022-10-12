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

    def __init__(self, *args, **kwargs):
        super(WorkOrderFilter, self).__init__(*args, **kwargs)
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

    def custom_search_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(brief_description__icontains=value)
                |Q(facility__name__icontains=value)
                |Q(asset__slug__icontains=value)
                |Q(location__specific_location__icontains=value)
                |Q(location__building__name__icontains=value)
                |Q(location__department__name__icontains=value)
                |Q(location__floor__number__icontains=value)
            )
        return queryset
