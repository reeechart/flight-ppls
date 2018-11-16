from django.contrib import admin
from .models import Payment
# Register your models here.
@admin.register(Payment)
class Payment(admin.ModelAdmin):
   actions = ['send_callback']
   def send_callback(self, request, queryset):
       for i in queryset:
           i.call(i.callback_url, i.callback_body)
