from rest_framework import serializers

from django.contrib.auth.models import User

from flight_booking.models import Flight
from flight_booking.models import Booking
from flight_booking.models import Invoice
from flight_booking.models import Ticket

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            'number',
            'origin',
            'destination',
            'departure',
            'arrival',
            'capacity',
            'available_seats',
            'price' 
        )

class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.SlugRelatedField(
        slug_field='number',
        queryset=Flight.objects.all()
    )
    user =  serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    passengers = serializers.JSONField()

    class Meta:
        model = Booking
        exclude = ('id', )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class InvoiceSerializer(serializers.ModelSerializer):
    booking = serializers.SlugRelatedField(
        slug_field='number',
        queryset=Booking.objects.all()
    )
    user =  serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Invoice
        exclude = ('id', )

class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.SlugRelatedField(
        slug_field='number',
        queryset=Flight.objects.all()
    )
    user =  serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'flight')
