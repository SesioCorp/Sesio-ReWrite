from django import forms
from systemandfacility.models import Location
from .models import WorkOrder

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["category", "description", "brief_description", "work_order_connected_to_an_asset", "enter_device_id_manually", "repair_images"]


class WorkOrderStatusForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["priority", "status", "completed_at"]