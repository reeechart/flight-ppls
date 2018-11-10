from django.db import models

# Create your models here.

class Flight(models.Model):
    origin = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    departure = models.DateTimeField(auto_now=False)
    arrival = models.DateTimeField(auto_now=False)
    available_seats = models.IntegerField(editable=True)