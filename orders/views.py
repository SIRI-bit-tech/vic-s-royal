from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
import urllib.parse
from io import BytesIO
import os
import requests

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart
            cart.clear()
            
            # Send order confirmation email to user
            send_order_confirmation_email(order)
            
            # Send order details to admin
            send_admin_order_email(order)
            
            # Redirect to WhatsApp
            whatsapp_url = generate_whatsapp_url(request, order)
            return redirect(whatsapp_url)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

def generate_whatsapp_url(request, order):
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'

    # Create a URL for the order details page
    order_details_url = f"{protocol}://{domain}{reverse('orders:admin_order_details', args=[order.id])}"

    message = f"New order received!\n\n"
    message += f"Order Number: #{order.id}\n"
    message += f"Invoice Number: {order.invoice_number}\n\n"
    message += f"Customer: {order.first_name} {order.last_name}\n"
    message += f"Email: {order.email}\n"
    message += f"Address: {order.address}, {order.postal_code} {order.city}\n\n"
    message += f"View full order details and images: {order_details_url}\n\n"
    message += f"Total: ₦{order.get_total_cost()}"
    
    whatsapp_number = settings.ADMIN_WHATSAPP
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{whatsapp_number}?text={encoded_message}"

def send_order_confirmation_email(order):
    subject = f'Order nr. {order.id}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email

    # Get the order items with their images
    order_items = []
    for item in order.items.all():
        image_url = item.product.image.url  # Use url instead of path for Cloudinary
        order_items.append({
            'product': item.product,
            'price': item.price,
            'quantity': item.quantity,
            'image_url': image_url,
        })

    # Prepare context for the email template
    context = {
        'order': order,
        'order_items': order_items,
        'support_email': settings.SUPPORT_EMAIL,
        'admin_whatsapp': settings.ADMIN_WHATSAPP,
    }

    html_message = render_to_string('order_confirmation_email.html', context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
    msg.attach_alternative(html_message, "text/html")

    try:
        msg.send()
        print("Order confirmation email sent successfully")
    except Exception as e:
        print(f"Error sending order confirmation email: {str(e)}")

def send_admin_order_email(order):
    subject = f'New Order Received - Order #{order.id}'
    html_message = render_to_string('admin_order_email.html', {
        'order': order,
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = settings.ADMIN_EMAIL

    msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")

    # Attach product images
    for item in order.items.all():
        if item.product.image:
            try:
                response = requests.get(item.product.image.url)
                if response.status_code == 200:
                    img_data = BytesIO(response.content)
                    msg.attach(f'{item.product.name}.png', img_data.getvalue(), 'image/png')
            except Exception as e:
                print(f"Error attaching image for {item.product.name}: {str(e)}")

    try:
        msg.send()
        print("Admin order email sent successfully")
    except Exception as e:
        print(f"Error sending admin order email: {str(e)}")

@login_required
def admin_order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/admin_order_details.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
