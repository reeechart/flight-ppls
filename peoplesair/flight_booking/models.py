from django.db import models

# Create your models here.

class Flight(models.Model):
    departure = models.CharField(max_length=255, blank=False)
    arrival = models.CharField(max_length=255, blank=False)
    departure_time = models.DateTimeField(auto_now=False)
    available_seats = models.IntegerField(editable=True)