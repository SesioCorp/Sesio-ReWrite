import django_filters
from .models import *

class FacilityFilter(django_filters.FilterSet):
    """facility filters"""

    class Meta:
        """meta class to add fields """

        models = Facility
        fields = {
            "name": ["icontains"],
            "description": ["icontains"],
            "short_description": ["exact"],
            "slug": ["exact"],
            "system": ["exact"],
        }

class BuildingFilter(django_filters.FilterSet):
    class Meta:
        model_name = Building
        fields = ["facility", "name"]

class FloorFilter(django_filters.FilterSet):
    class Meta:
        model_name = Floor
        fields = ["facility", "building", "number", "name"]

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model_name = Department
        fields = ["facility", "building", "floor", "name"]

