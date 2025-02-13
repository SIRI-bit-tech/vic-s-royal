from django.contrib import admin
from .models import (
    Category, Product, Review, Wishlist,
    HeroBanner, Testimonial, BlogPost,
    InstagramFeed, Video
)
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'get_product_count', 'display_image']
    list_filter = ['active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = 'Products'

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'current_price_display', 'on_sale', 
                   'available', 'featured', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'on_sale', 'featured']
    list_editable = ['price', 'available', 'featured', 'on_sale']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'available'),
            'classes': ('collapse',)
        }),
        ('Sale Information', {
            'fields': ('on_sale', 'discount_percentage', 'sale_price', 
                      'sale_start_date', 'sale_end_date'),
            'classes': ('collapse',)
        }),
        ('Product Details', {
            'fields': ('size', 'length', 'color', 'featured'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

    def current_price_display(self, obj):
        if obj.on_sale and obj.sale_price:
            return format_html(
                '<span style="text-decoration: line-through">₦{}</span> '
                '<span style="color: red">₦{}</span>',
                obj.price, obj.sale_price
            )
        return f'₦{obj.price}'
    current_price_display.short_description = 'Current Price'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['product__name', 'user__username', 'comment']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'get_product_count']
    search_fields = ['user__username']

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = 'Products'

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order', 'display_image', 'created']
    list_editable = ['active', 'order']
    search_fields = ['title', 'subtitle']
    list_filter = ['active', 'created']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Banner Image'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'active', 'display_image', 'created']
    list_editable = ['active']
    search_fields = ['name', 'content']
    list_filter = ['rating', 'active', 'created']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'display_image', 'created']
    list_editable = ['active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']
    list_filter = ['active', 'created']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(InstagramFeed)
class InstagramFeedAdmin(admin.ModelAdmin):
    list_display = ['caption', 'active', 'display_image', 'created']
    list_editable = ['active']
    search_fields = ['caption']
    list_filter = ['active', 'created']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'display_thumbnail', 'created']
    list_editable = ['active']
    search_fields = ['title', 'description']
    list_filter = ['active', 'created']

    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" />', obj.thumbnail.url)
        return "No thumbnail"
    display_thumbnail.short_description = 'Thumbnail'

