from django import forms
from systemandfacility.models import Location
from .models import WorkOrder
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["category", "description", "brief_description", "work_orders_connected_to_an_asset", "enter_device_id_manually", "repair_images"]
        labels = {
            "category": _("Work Order Category"),
            "description": _("Description of Issue/Repair"),
            "brief_description": _("Brief Description of Work Order"),
            "work_orders_connected_to_an_asset": _("Is the work order connected to an asset?"),
            "repair_images": _("Picture of Issue/Repair")
        }

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
        fields = ["priority", "status", "assigned_to", "completed_at", "timespent"]
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

class WorkOrderAssignForm(forms.Form):
    requester = forms.ModelChoiceField(label="Requester", queryset=CustomUser.objects.filter(), required=False)