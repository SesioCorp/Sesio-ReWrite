from django.db import models
from django.conf import settings

from systemandfacility.models import Facility, Location
from asset.models import Asset

PREVENTIVE_MAINTAINENCE_STATUS = (
    ("ready_to_start", "Ready to start"),
    ("in_progress", "In progress"),
    ("waiting_for_approval", "Wait for Approval"),
    ("complete", "Complete"),
)
FREQUENCY = (
    ("every_day", "Every Day"),
    ("every_week", "Every Week"),
    ("monthly", "Monthly"),
    ("quaterly", "Quaterly"),
    ("semi", "Semi"),
    ("annual", "Annual"),
    ("tri-annual", "Tri-Annual"),
    ("5-years", "5-Year"),
)


class PreventiveMaintenance(models.Model):
    slug = models.SlugField(unique=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="preventive_maintenances")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="preventive_maintenance")
    status = models.CharField(choices=PREVENTIVE_MAINTAINENCE_STATUS, default="ready_to_start", max_length=50)
    frequency = models.CharField(choices=FREQUENCY, default="monthly", max_length=50)
    started_at = models.DateTimeField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    image = models.FileField(upload_to="images/")

    def __str__(self):
        return self.slug
