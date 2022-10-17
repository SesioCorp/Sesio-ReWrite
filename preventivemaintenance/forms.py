from django import forms

from asset.models import AssetType
from .models import PreventiveMaintenance


class PreventiveMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenance
        fields = ['slug', 'facility', 'asset', 'status', 'frequency', 'started_at', 'expired_at', 'image']

class PreventiveMaintenanceAssetDetailsForm(forms.Form):
    asset_type = forms.ModelChoiceField(label="Type", queryset=AssetType.objects.all())
    weight = forms.IntegerField(label="Weight")
    brand = forms.CharField(label="Brand", max_length=100)
    

