from rest_framework import serializers

from flight_booking.models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ('id', )