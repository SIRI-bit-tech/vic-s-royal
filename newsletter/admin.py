from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_subscribed']
    list_filter = ['date_subscribed']
    search_fields = ['email']

