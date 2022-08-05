from django.db import models


# Create your models here.
class Map(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to="map/images/")

    def __str__(self):
        return self.name