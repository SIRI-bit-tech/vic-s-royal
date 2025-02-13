from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = CloudinaryField('image', folder='categories', null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        original_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('N', 'None'),
    ]
    LENGTH_CHOICES = [
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('none', 'None'),
    ]

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = CloudinaryField('image', folder='products', 
                          transformation={
                              'width': 800,
                              'height': 600,
                              'crop': 'fill',
                              'quality': 'auto',
                              'fetch_format': 'auto'
                          })
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in Naira (₦)')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='M')
    length = models.CharField(max_length=10, choices=LENGTH_CHOICES, default='medium')
    color = models.CharField(max_length=50, blank=True)
    featured = models.BooleanField(default=False, help_text='Check to display this product on the homepage')
    meta_description = models.CharField(max_length=160, blank=True, help_text='Meta description for SEO (max 160 characters)')
    meta_keywords = models.CharField(max_length=255, blank=True, help_text='Comma-separated keywords for SEO')
    
    # Sale fields
    on_sale = models.BooleanField(default=False, help_text='Check to put this product on sale')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Sale price in Naira (₦)')
    sale_start_date = models.DateTimeField(null=True, blank=True)
    sale_end_date = models.DateTimeField(null=True, blank=True)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True, help_text='Discount percentage (0-100)')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['featured']),
            models.Index(fields=['on_sale']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Calculate sale price if discount percentage is provided
        if self.discount_percentage and self.price:
            discount = (Decimal(self.discount_percentage) / Decimal(100)) * self.price
            self.sale_price = self.price - discount

        super().save(*args, **kwargs)

    @property
    def current_price(self):
        """Returns the current price (sale price if on sale, regular price otherwise)"""
        if self.on_sale and self.sale_price:
            return self.sale_price
        return self.price

    @property
    def savings_amount(self):
        """Returns the amount saved when the product is on sale"""
        if self.on_sale and self.sale_price:
            return self.price - self.sale_price
        return Decimal('0')

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class HeroBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = CloudinaryField('image', folder='banners',
                          transformation={
                              'width': 1920,
                              'height': 800,
                              'crop': 'fill',
                              'quality': 'auto',
                              'fetch_format': 'auto'
                          })
    button_text = models.CharField(max_length=50, default='Shop Now')
    button_link = models.CharField(max_length=200, default='/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='testimonials', null=True, blank=True,
                          transformation={
                              'width': 150,
                              'height': 150,
                              'crop': 'fill',
                              'quality': 'auto',
                              'fetch_format': 'auto'
                          })
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Testimonial by {self.name}'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = CloudinaryField('image', folder='blog',
                          transformation={
                              'width': 1200,
                              'height': 630,
                              'crop': 'fill',
                              'quality': 'auto',
                              'fetch_format': 'auto'
                          })
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:blog_detail', args=[self.slug])

class InstagramFeed(models.Model):
    image = CloudinaryField('image', folder='instagram',
                          transformation={
                              'width': 600,
                              'height': 600,
                              'crop': 'fill',
                              'quality': 'auto',
                              'fetch_format': 'auto'
                          })
    caption = models.CharField(max_length=200)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.caption

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text='YouTube or Vimeo URL')
    thumbnail = CloudinaryField('image', folder='video_thumbnails', null=True, blank=True,
                             transformation={
                                 'width': 1280,
                                 'height': 720,
                                 'crop': 'fill',
                                 'quality': 'auto',
                                 'fetch_format': 'auto'
                             })
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

