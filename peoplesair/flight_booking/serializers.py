from rest_framework import serializers

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