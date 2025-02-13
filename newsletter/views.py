from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubscriberForm

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter!')
            return redirect('home')
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/subscribe.html', {'form': form})

