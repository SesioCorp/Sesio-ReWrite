from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Building, Department, Floor
from .filters import *
from django.contrib.auth.mixins import LoginRequiredMixin

class BuildingListView(LoginRequiredMixin, ListView):
    model = Building

    def get_queryset(self):
        if self.request.is_ajax():
            if self.request.GET.get("facility"):
                return self.model.objects.filter(facility_id=self.request.GET.get("facility"))
            else:
                return self.model.objects.none()
        queryset = self.model.objects.all()
        filter_queryset = BuildingFilter(self.request.GET, queryset=queryset)
        return filter_queryset
        
    def get_template_names(self):
        if self.request.is_ajax():
            return "partials/dropdown_list.html"

class FloorListView(LoginRequiredMixin, ListView):
    model = Floor

    def get_queryset(self):
        if self.request.is_ajax():
            if self.request.GET.get("building"):
                return self.model.objects.filter(building_id=self.request.GET.get("building"))
            else:
                return self.model.objects.none()
        queryset = self.model.objects.all()
        filter_queryset = FloorFilter(self.request.GET, queryset=queryset)
        return filter_queryset
        
    def get_template_names(self):
        if self.request.is_ajax():
            return "partials/dropdown_list.html"

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department

    def get_queryset(self):
        if self.request.is_ajax():
            if self.request.GET.get("floor"):
                return self.model.objects.filter(floor_id=self.request.GET.get("floor"))
            else:
                return self.model.objects.none()
        queryset = self.model.objects.all()
        filter_queryset = DepartmentFilter(self.request.GET, queryset=queryset)
        return filter_queryset
       
    def get_template_names(self):
        if self.request.is_ajax():
            return "partials/dropdown_list.html"