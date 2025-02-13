from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'is_active']
    list_filter = ['created_at', 'is_active']
    search_fields = ['email']
    readonly_fields = ['created_at']
    list_per_page = 25