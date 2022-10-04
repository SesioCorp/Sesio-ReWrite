from django.shortcuts import render
from .models import PreventiveMaintenance
from .filters import PreventiveMaintenanceFilter

class PreventiveMaintenanceListView(ListView):
    model = PreventiveMaintenance
    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.is_ajax():
            filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
            return filtered_queryset.qs

        queryset = self.model.objects.all().order_by('-updated_at')
        filtered_queryset = PreventiveMaintenanceFilter(self.request.GET, queryset=queryset)
        return filtered_queryset.qs

    def get_template_names(self):
        if self.request.is_ajax():
            return 'workorder/partials/dropdown_list.html'
        return 'preventivemaintenance_listview.html'

