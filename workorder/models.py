from datetime import datetime
from django.db import models
from systemandfacility.models import Facility, Location
from asset.models import *
from django.conf import settings

AssetChoices = (("no", "No"), ("yes", "Yes"))
Choices =(("open", "Open"), ("closed", "Closed"))

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



class WorkOrder(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="work_orders")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="work_orders")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="work_orders")
    brief_description =models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="work_orders")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="work_orders", blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    enter_device_id_manually = models.CharField(max_length=100, blank=True, null=True)
    asset = models.ManyToManyField(Asset, related_name="work_orders", blank=True)
    repair_images = models.ImageField(upload_to="uploads/", blank=True)
    status = models.CharField(max_length=50, choices=Choices, blank=False, default="open")
    scan_bar_code = models.CharField(max_length=50, blank=True)
    work_orders_connected_to_an_asset=models.CharField(max_length=50, choices=AssetChoices, blank=True, default="no")
    timespent = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.brief_description

class Comment(models.Model):
    comment = models.TextField()
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="comments")


class TimeSpent(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    workorder = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, related_name="time_spent")

    def __str__(self):
        return f"{self.start_time} {self.end_time}"