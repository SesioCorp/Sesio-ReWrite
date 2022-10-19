from django.db import models
from systemandfacility.models import Facility, Location
from question.models import QuestionSet

class AssetAttributeSet(models.Model):
    weight = models.IntegerField()
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.brand

class AssetType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="assets")
    attribute_set = models.ForeignKey(AssetAttributeSet, on_delete=models.CASCADE, related_name="assets")
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name="assets")
    slug = models.SlugField(unique=True)
    device_id = models.CharField(max_length=100)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name="assets")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="assets", null=True, blank=True)
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return self.asset_type.name




    

