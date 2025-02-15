from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Product, Review, Wishlist, HeroBanner, Testimonial, BlogPost, Video
from cart.forms import CartAddProductForm
from .forms import ReviewForm
from django.utils import timezone
from django.db.models import Count
from django.core.cache import cache
from django.db.models import Prefetch

def home(request):
    # Hero Banners
    hero_banners = HeroBanner.objects.filter(active=True).order_by('order')[:3]
    
    # Featured Products
    featured_products = Product.objects.filter(
        featured=True,
        available=True
    )[:8]
    
    # Special Offers (Products on Sale)
    special_offers = Product.objects.filter(
        on_sale=True,
        available=True,
        sale_start_date__lte=timezone.now(),
        sale_end_date__gte=timezone.now()
    )[:4]
    
    # New Arrivals (Products added in the last 30 days)
    new_arrivals = Product.objects.filter(
        available=True,
        created__gte=timezone.now() - timezone.timedelta(days=30)
    ).order_by('-created')[:4]
    
    # Customer Testimonials
    testimonials = Testimonial.objects.filter(active=True)[:6]
    
    # All Categories
    categories = Category.objects.all().annotate(
        product_count=Count('products')
    )
    
    # Best Sellers (using featured flag for now, could be enhanced with order data)
    best_sellers = Product.objects.filter(
        featured=True,
        available=True
    ).order_by('?')[:4]
    
    # Hair Care Tips (Blog Posts)
    hair_care_tips = BlogPost.objects.filter(active=True)[:3]
    
    # Tutorial Videos
    tutorial_videos = Video.objects.filter(active=True)[:2]

    return render(request, 'home.html', {
        'hero_banners': hero_banners,
        'featured_products': featured_products,
        'special_offers': special_offers,
        'new_arrivals': new_arrivals,
        'testimonials': testimonials,
        'categories': categories,
        'best_sellers': best_sellers,
        'hair_care_tips': hair_care_tips,
        'tutorial_videos': tutorial_videos,
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category').prefetch_related(
        'reviews',
        'variants',
        Prefetch('wishlist_set', queryset=Wishlist.objects.filter(user=request.user if request.user.is_authenticated else None))
    )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Caching the queryset
    products = cache.get_or_set(
        f'products_list_{category_slug}_{request.user.id if request.user.is_authenticated else "anon"}',
        products,
        timeout=3600
    )
    
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.select_related('category')
        .prefetch_related(
            'reviews__user',
            'variants',
            'related_products',
            Prefetch('wishlist_set', queryset=Wishlist.objects.filter(user=request.user if request.user.is_authenticated else None))
        ),
        id=id,
        slug=slug,
        available=True
    )
    
    # Cache the product detail
    cache_key = f'product_detail_{id}_{slug}_{request.user.id if request.user.is_authenticated else "anon"}'
    product = cache.get_or_set(cache_key, product, timeout=3600)
    
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'review_form': review_form
    })

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
    return redirect('products:product_detail', id=product.id, slug=product.slug)

def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
    })

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'wishlist_total': wishlist.products.count()})
    return redirect('products:product_detail', id=product.id, slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'wishlist_total': wishlist.products.count()})
    return redirect('products:wishlist')

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist': wishlist})

@login_required
def wishlist_count(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return JsonResponse({'count': wishlist.products.count()})

def faq(request):
    return render(request, 'faq.html')

def customer_support(request):
    return render(request, 'customer_support.html')

def send_support_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'Support message from {name}',
            f'From: {email}\n\nMessage: {message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
        
        # Redirect to a thank you page or back to the support page with a success message
        return render(request, 'customer_support.html', {'message_sent': True})
    
    # If not POST, redirect to the customer support page
    return redirect('customer_support')

def about(request):
    return render(request, 'about.html')

def blog_detail(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug, active=True)
    
    # Get related posts (posts with similar tags or in the same category)
    # Exclude the current post and limit to 2 posts
    related_posts = BlogPost.objects.filter(
        active=True
    ).exclude(
        id=blog_post.id
    ).order_by('-created')[:2]
    
    return render(request, 'products/blog_detail.html', {
        'post': blog_post,
        'related_posts': related_posts
    })
