from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from .forms import NewsletterForm
from .models import Subscriber

@require_http_methods(["POST"])
def subscribe(request):
    # Check if request is AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        
        # Check if already subscribed
        if Subscriber.objects.filter(email=email).exists():
            response_data = {
                'status': 'error',
                'message': 'You are already subscribed to our newsletter!'
            }
            return JsonResponse(response_data) if is_ajax else redirect('home')
        
        try:
            # Create new subscriber
            subscriber = form.save()
            
            # Send confirmation email
            html_message = render_to_string('newsletter/confirmation_email.html')
            send_mail(
                subject='Welcome to Vic\'s Royal Beauty Newsletter!',
                message='Thank you for subscribing to our newsletter!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            response_data = {
                'status': 'success',
                'message': 'Thank you for subscribing! Please check your email for confirmation.'
            }
            
            if not is_ajax:
                messages.success(request, response_data['message'])
                return redirect('home')
                
            return JsonResponse(response_data)
            
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': 'An error occurred. Please try again later.'
            }
            return JsonResponse(response_data) if is_ajax else redirect('home')
    else:
        response_data = {
            'status': 'error',
            'message': 'Please enter a valid email address.'
        }
        return JsonResponse(response_data) if is_ajax else redirect('home')

