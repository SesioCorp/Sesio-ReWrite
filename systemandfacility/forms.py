from socket import fromshare
from django import forms
from .models import Location, Building, Floor, Department

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["facility", "building", "floor", "department", "specific_location"]

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields["building"].queryset = Building.objects.none()
        self.fields["floor"].queryset = Floor.objects.none()
        self.fields["department"].queryset = Department.objects.none()

        if "LocationForm-facility" in self.data:
            try:
                _facility_id = int(self.data.get("LocationForm-facility"))
                self.fields["building"].queryset = Building.objects.filter(facility_id=_facility_id)
            except:
                pass

        elif self.instance.pk:
            self.fields["building"].queryset = Building.objects.filter(id=self.instance.pk)

        if "LocationForm-building" in self.data:
            try:
                _building_id = int(self.data.get("LocationForm-building"))
                self.fields["floor"].queryset = Floor.objects.filter(building_id=_building_id)
            except:
                pass

        elif self.instance.pk:
            self.fields["floor"].queryset = Floor.objects.filter(id=self.instance.pk)

        if "LocationForm-floor" in self.data:
            try:
                _floor_id = int(self.data.get("LocationForm-floor"))
                self.fields["department"].queryset = Department.objects.filter(floor_id=_floor_id)
            except:
                pass
        
        elif self.instance.pk:
            self.fields["department"].queryset = Department.objects.filter(id=self.instance.pk)