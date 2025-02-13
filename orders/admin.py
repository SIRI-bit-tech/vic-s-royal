from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city',
                    'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='order_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        recent_orders = Order.objects.order_by('-created')[:10]
        context = {
            'recent_orders': recent_orders,
            'title': 'Order Dashboard',
        }
        return render(request, 'admin/orders/order/dashboard.html', context)

