from django.db import models


class System(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name="facilities")

    def __str__(self):
        return self.name