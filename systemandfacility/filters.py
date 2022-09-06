import django_filters
from .models import *

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
