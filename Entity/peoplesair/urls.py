"""peoplesair URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from flight_booking.views import FlightListView
from flight_booking.views import FlightView
from flight_booking.views import BookingListView
from flight_booking.views import BookingView
from flight_booking.views import UserView
from flight_booking.views import UserListView
from flight_booking.views import InvoiceListView
from flight_booking.views import TicketView
from flight_booking.views import MockNotifyPayment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', FlightListView.as_view(), name='flight-list'),
    path('flights/<slug:number>/', FlightView.as_view(), name='flight'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<slug:number>/', BookingView.as_view(), name='booking'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<slug:id>/', UserView.as_view(), name='user'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('tickets/', TicketView.as_view(), name='ticket-list'),
    path('mock-notify-payment/', MockNotifyPayment.as_view(), name="mock-notify-payment")
]
