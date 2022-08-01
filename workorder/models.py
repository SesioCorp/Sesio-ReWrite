from django.db import models
from systemandfacility.models import Facility, Location
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='child', null=True, blank=True)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name



# class WorkOrder(models.Model):
#     facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="work_orders")
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="work_orders")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="work_orders")
#     brief_discription =models.CharField(max_length=50)
#     discription = models.TextField(blank=True, null=True)
#     priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="work_orders")
#     assigned = ForeignKey