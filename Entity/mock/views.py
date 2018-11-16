from django.shortcuts import render
from .models import Payment
from rest_framework.views import APIView
from django.http import HttpResponse

# Create your views here.
class PaymentView(APIView):
    def post(self, request):
        callback_url = request.data.get("callback_url")
        callback_body = request.data.get("callback_body")
        payment = Payment()
        payment.callback_url = callback_url
        payment.callback_body = callback_body
        payment.save()
        return HttpResponse(status=201)
        
        
