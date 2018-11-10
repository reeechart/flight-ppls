from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class Flight(models.Model):
    number = models.CharField(_('Number'), max_length=128, unique=True)
    origin = models.CharField(_('Origin'), max_length=128)
    destination = models.CharField(_('Destination'), max_length=128)
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    available_seats = models.IntegerField(_('Available Seats'))

class Booking(models.Model):
    number = models.CharField(_('Number'), max_length=128, unique=True)
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, related_name='bookings', on_delete=models.CASCADE)



