from django.contrib import admin
from .models import System, Facility, Building, Floor, Location, Department

admin.site.register(System)
admin.site.register(Facility)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Location)
admin.site.register(Department)