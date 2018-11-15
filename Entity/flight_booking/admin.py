from django.contrib import admin
from django.contrib.auth.models import User
from .models import Flight, Invoice, Ticket, Booking
# Register your models here.

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
