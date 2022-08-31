from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Building, Department, Floor

class BuildingListView(ListView):
    model = Building

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

class FloorListView(ListView):
    model = Floor

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

class DepartmentListView(ListView):
    model = Department

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset