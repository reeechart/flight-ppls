from django.db import models
from django.utils.translation import ugettext_lazy as _

class Flight(models.Model):
    origin = models.CharField(_('Origin'), max_length=128)
    destination = models.CharField(_('Destination'), max_length=128)
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    available_seats = models.IntegerField(_('Available Seats'))
