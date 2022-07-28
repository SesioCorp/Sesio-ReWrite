from django.contrib import admin
from .models import System, Facility, Building, Floor

admin.site.register(System)
admin.site.register(Facility)
admin.site.register(Building)
admin.site.register(Floor)