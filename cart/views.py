from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                update_quantity=cd['override'])
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'cart_total': cart.get_total_quantity(),
                'item_quantity': cart.get_item_quantity(product_id),
                'item_total': cart.get_item_total(product_id),
                'cart_total_price': cart.get_total_price(),
                'cart_discount': cart.get_discount() or '0'
            })
        return redirect('cart:cart_detail')
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'cart_total': cart.get_total_quantity(),
            'item_quantity': 0,
            'cart_total_price': cart.get_total_price(),
            'cart_discount': cart.get_discount() or '0'
        })
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_count(request):
    cart = Cart(request)
    return JsonResponse({'count': cart.get_total_quantity()})

@login_required
def cart_increase(request, product_id):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=1, update_quantity=False)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'cart_total': cart.get_total_quantity(),
                'item_quantity': cart.get_item_quantity(product_id),
                'item_total': cart.get_item_total(product_id),
                'cart_total_price': cart.get_total_price(),
                'cart_discount': cart.get_discount() or '0'
            })
        return redirect('cart:cart_detail')

@login_required
def cart_decrease(request, product_id):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.decrease(product=product)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'cart_total': cart.get_total_quantity(),
                'item_quantity': cart.get_item_quantity(product_id),
                'item_total': cart.get_item_total(product_id),
                'cart_total_price': cart.get_total_price(),
                'cart_discount': cart.get_discount() or '0'
            })
        return redirect('cart:cart_detail')

