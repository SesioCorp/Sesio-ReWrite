from django.shortcuts import render
from .models import PreventiveMaintenance
from .filters import PreventiveMaintenanceFilter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class PreventiveMaintenanceListView(ListView):
   
    model = PreventiveMaintenance
   
    def get_queryset(self):

        if self.request.is_ajax():
            queryset = self.model.objects.all()
            filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
            return filtered_queryset.qs

        queryset = self.model.objects.all()
        filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
        return filtered_queryset

    def get_template_names(self):
        if self.request.is_ajax():
            return 'preventivemaintenance/partials/dropdown_list.html'
        return 'preventivemaintenance_listview.html'

class PreventiveMaintenanceDetailView(DetailView):
    model = PreventiveMaintenance
    template_name = "preventivemaintenance_detail.html"