from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order

@staff_member_required
def admin_dashboard(request):
    recent_orders = Order.objects.order_by('-created')[:10]
    context = {
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

