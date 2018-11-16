from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

import requests

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

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

class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get(self, request):
        if request.query_params:
            first_name = request.query_params.get('first-name')
            last_name = request.query_params.get('last-name')
            flight_number = request.query_params.get('flight-number')
            ticket = get_object_or_404(
                Ticket,
                first_name=first_name,
                last_name=last_name,
                flight__number=flight_number
            )
            return Response(TicketSerializer(ticket).data, status=200)
        else:
            return super().get(request)
        

class MockNotifyPayment(APIView):
    def post(self, request):
        booking_number = request.data.get("booking_number")
        callback_url = request.data.get("callback_url")
        request = requests.post(callback_url, data={status:"paid"})

