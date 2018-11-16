from rest_framework import generics
from rest_framework.views import APIView

import requests

from django.contrib.auth.models import User

from flight_booking.models import Flight
from flight_booking.models import Booking
from flight_booking.models import Invoice
from flight_booking.models import Ticket

from flight_booking.serializers import FlightSerializer
from flight_booking.serializers import BookingSerializer
from flight_booking.serializers import UserSerializer
from flight_booking.serializers import InvoiceSerializer
from flight_booking.serializers import TicketSerializer

class FlightListView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightView(generics.RetrieveUpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    lookup_field = 'number'

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingView(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'number'

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class InvoiceListView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class TicketListView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'id'

class MockNotifyPayment(APIView):
    def post(self, request):
        booking_number = request.data.get("booking_number")
        callback_url = request.data.get("callback_url")
        request = requests.post(callback_url, data={status:"paid"})

