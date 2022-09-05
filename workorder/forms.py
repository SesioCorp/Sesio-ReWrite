from django import forms
from systemandfacility.models import Location
from .models import WorkOrder

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["category", "description", "brief_description", "work_orders_connected_to_an_asset", "enter_device_id_manually", "repair_images"]


class WorkOrderStatusForm(forms.ModelForm):
    completed_at = forms.DateTimeField(
        label = "Date Completed",
        widget = forms.DateInput(
            format=("%Y/%m/%d"),
            attrs={
                "class": "form-control",
                "type": "date"
            }
        ),
        required = False
    )


    class Meta:
        model = WorkOrder
        fields = ["priority", "status", "assigned_to", "completed_at"]
        widgets = {
            "priority": forms.RadioSelect(),
            "status": forms.RadioSelect(),
            "completed_at": forms.DateInput(
                format = ("%Y/%m/%d"),
                attrs = {
                    "class": "form-control",
                    "type": "date"
                }
            ),

        }