from django import forms
from .models import PreventiveMaintenance


class PreventiveMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenance
        fields = ['slug', 'facility', 'asset', 'status', 'frequency', 'started_at', 'expired_at', 'images']