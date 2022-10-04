from django.urls import path
from .views import PreventiveMaintenanceListView
from .forms import PreventiveMaintenanceForm

Forms = [
    ("PreventiveMaintenanceFrom", PreventiveMaintenanceForm)
    ]

urlpatterns = [
    path('list/', PreventiveMaintenanceListView.as_view(), name='preventive_maintenance_list')
]