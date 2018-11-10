from rest_framework import generics

from flight_booking.models import Flight
from flight_booking.serializers import FlightSerializer

class FlightListView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightView(generics.RetrieveUpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer    
