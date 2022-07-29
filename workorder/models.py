from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='child', null=True, blank=True)
    order = models.IntegerField()

    def __str__(self):
        return self.name