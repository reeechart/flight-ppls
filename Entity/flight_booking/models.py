from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
import json

from django.contrib.auth.models import User

class Flight(models.Model):
    number = models.CharField(_('Number'), max_length=128, unique=True)
    origin = models.CharField(_('Origin'), max_length=128)
    destination = models.CharField(_('Destination'), max_length=128)
    departure = models.DateTimeField(_('Departure'))
    arrival = models.DateTimeField(_('Arrival'))
    capacity = models.PositiveIntegerField(_('Available Seats'))
    price = models.FloatField(_('Price'))
    
    @property
    def available_seats(self):
        bookings = Booking.objects.filter(flight__number=self.number).exclude(status=Booking.CANCELED)
        occupied_seats = 0
        for booking in bookings:
            occupied_seats += len(booking.passengers)
        return self.capacity - occupied_seats
    
class Booking(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    CANCELED = 'canceled'

    STATUS_CHOICES = (
        (PENDING, _('pending')),
        (PAID, _('paid')),
        (CANCELED, _('canceled')),
    )
    
    number = models.CharField(_('Number'), max_length=128, unique=True)
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, related_name='bookings', on_delete=models.CASCADE)
    passengers = JSONField(_('Passengers'))
    status = models.CharField(_('Status'), max_length=128, choices=STATUS_CHOICES)

class Invoice(models.Model):
    user = models.ForeignKey(User, related_name='invoices', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='invoices', on_delete=models.CASCADE)
    price = models.IntegerField(_('Price'))

class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, related_name='tickets', on_delete=models.CASCADE)
    first_name = models.CharField(_('First Name'), max_length=128)
    last_name = models.CharField(_('Last Name'), max_length=128)