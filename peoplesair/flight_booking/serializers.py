from rest_framework import serializers

from django.contrib.auth.models import User

from flight_booking.models import Flight
from flight_booking.models import Booking


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ('id', )

class BookingSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()

    class Meta:
        model = Booking
        exclude = ('id', )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')