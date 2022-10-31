from django.urls import reverse
from django.shortcuts import render
from .models import PreventiveMaintenance
from .filters import PreventiveMaintenanceFilter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from systemandfacility.forms import LocationForm
from .forms import PreventiveMaintenanceAssetDetailsForm
from asset.models import *
from django.http import HttpResponseRedirect

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
        import pdb; pdb.set_trace()
        context["asset_update"] = PreventiveMaintenanceAssetDetailsForm(initial=self.pm_asset_details())
        return context

    def pm_asset_details(self):
        try:
            data = {
                "asset_type": self.get_object().asset.asset_type,
                "weight": self.get_object().asset.attribute_set.weight,
                "brand": self.get_object().asset.attribute_set.brand
            }

        except Asset.DoesNotExist: 
            data = {
                "asset_type": None,
                "weight": None,
                "brand": None
            }

        return data

    def post(self, request, *args, **kwargs):
        location_form = LocationForm(self.request.POST)
        asset_form = PreventiveMaintenanceAssetDetailsForm(self.request.POST)

        if location_form.is_valid():
            object_data = self.get_object()
            if object_data.asset.location:
                object_data.facility = location_form.cleaned_data['facility']
                object_data.asset.location.building = location_form.cleaned_data['building']
                object_data.asset.location.floor = location_form.cleaned_data['floor']
                object_data.asset.location.department = location_form.cleaned_data['department']
                object_data.asset.location.specific_location = location_form.cleaned_data['specific_location']
                object_data.asset.location.save()
                object_data.facility.save()
                object_data.save()
        
        if asset_form.is_valid():
            object_data = self.get_object()
            if object_data.asset:
                object_data.asset.asset_type = asset_form.cleaned_data['asset_type']
                object_data.asset.attribute_set.weight = asset_form.cleaned_data['weight']
                object_data.asset.attribute_set.brand = asset_form.cleaned_data['brand']
                object_data.asset.asset_type.save()
                object_data.asset.attribute_set.save()
                object_data.save()

        return HttpResponseRedirect(reverse("preventivemaintenance:preventive_maintenance_list"))