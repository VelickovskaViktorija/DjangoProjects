# FILE: models.py
# Овде се дефинираат сите модели: Agent, Feature, Property
from django.db import models

class Agent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    linkedin = models.URLField()
    email = models.EmailField(unique=True)
    sales_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Feature(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.value})"

class Property(models.Model):
    name = models.CharField(max_length=100)
    location_description = models.TextField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    listed_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='properties/')
    is_reserved = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    features = models.ManyToManyField(Feature, blank=True)
    agents = models.ManyToManyField(Agent, related_name="properties")

    def __str__(self):
        return f"{self.name} - {self.area} sqm"

    def total_price(self):
        return sum(f.value for f in self.features.all())