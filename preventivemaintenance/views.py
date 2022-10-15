from django.shortcuts import render
from .models import PreventiveMaintenance
from .filters import PreventiveMaintenanceFilter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from systemandfacility.forms import LocationForm
from .forms import PreventiveMaintenanceAssetDetailsForm
from asset.models import *

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

    def get_context_data(self, **kwargs):
        context = super(PreventiveMaintenanceDetailView, self).get_context_data(**kwargs)
        context["location_form"] = LocationForm(instance=self.get_object().asset.location)
        context["asset_update"] = PreventiveMaintenanceAssetDetailsForm(initial=self.pm_asset_details())
        return context

    def pm_asset_details(self):
        try:
            data = {
                "type": self.get_object().asset.asset_type,
                "weight": self.get_object().asset.attribute_set.weight,
                "brand": self.get_object().asset.attribute_set.brand
            }

        except Asset.DoesNotExist: 
            data = {
                "type": None,
                "weight": None,
                "brand": None
            }

        return data            