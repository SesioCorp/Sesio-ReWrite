from django.db import models
from common.models import BaseModel


class System(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Facility(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="facilities")

    def __str__(self):
        return self.name


class Building(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="buildings")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Floor(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="floors")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="floors")
    number = models.IntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Department(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="departments")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="departments")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Location(BaseModel):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="locations")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="locations")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="locations")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="locations")
    specific_location = models.CharField(max_length=50)

    def __str__(self):
        return self.specific_location