from tkinter import CASCADE
from django.db import models
from systemandfacility.models import Facility
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
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name="assets")
    slug = models.SlugField(unique=True)
    barcode = models.IntegerField()
    question_set = models.ForeignKey(QuestionSet, on_delete=CASCADE, related_name="assets")
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return self.type.name




    

