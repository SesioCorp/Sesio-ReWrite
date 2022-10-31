from django import forms
from .models import Location, Building, Floor, Department
from django.utils.translation import gettext_lazy as _


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["facility", "building", "floor", "department", "specific_location"]
        labels = {
            "specific_location": _("Specific Location")
        }

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields["building"].queryset = Building.objects.none()
        self.fields["floor"].queryset = Floor.objects.none()
        self.fields["department"].queryset = Department.objects.none()

        if "LocationForm-facility" in self.data:
            try:
                facility_id = int(self.data.get("LocationForm-facility"))
                self.fields["building"].queryset = Building.objects.filter(facility_id=facility_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["building"].queryset = Building.objects.filter(id=self.instance.building.id)
        else:
            self.fields["building"].queryset = Building.objects.all()

        if "LocationForm-building" in self.data:
            try:
                building_id = int(self.data.get("LocationForm-building"))
                self.fields["floor"].queryset = Floor.objects.filter(building_id=building_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["floor"].queryset = Floor.objects.filter(id=self.instance.floor.id)

        else:
            self.fields['floor'].queryset = Floor.objects.all()

        if "LocationForm-floor" in self.data:
            try:
                floor_id = int(self.data.get("LocationForm-floor"))
                self.fields["department"].queryset = Department.objects.filter(floor_id=floor_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["department"].queryset = Department.objects.filter(id=self.instance.department.id)
        else:
            self.fields["department"].queryset = Department.objects.all()