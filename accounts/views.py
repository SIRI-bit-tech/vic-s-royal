from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserEditForm
from orders.models import Order
from products.models import Wishlist, Product
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', reverse('home'))
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'accounts/login.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to Vic\'s Royal Beauty.')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Error during registration. Please try again.')
                return render(request, 'accounts/register.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    orders_list = Order.objects.filter(user=request.user).order_by('-created')
    
    # Pagination for orders
    page = request.GET.get('page', 1)
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.products.all()
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'wishlist_items': wishlist_items
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    messages.success(request, f"{product.name} has been removed from your wishlist.")
    return redirect('accounts:profile')

