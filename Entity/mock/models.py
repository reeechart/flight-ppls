from django.db import models
import requests

# Create your models here.
class Payment(models.Model):
    callback_url = models.CharField(max_length=128)
    callback_body = models.CharField(max_length=128)
    
    @classmethod
    def call(self, url, body):
        print("Sending message")
        request = requests.post(url, data=body)
        print(request)
