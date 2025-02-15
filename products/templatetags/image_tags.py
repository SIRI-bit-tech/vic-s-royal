from django import template
from django.templatetags.static import static
from cloudinary.utils import cloudinary_url

register = template.Library()

@register.simple_tag
def optimized_img(image_field, **options):
    if not image_field:
        return ''
    
    default_options = {
        'fetch_format': 'auto',
        'quality': 'auto',
        'loading': 'lazy',
        'flags': 'progressive',
    }
    
    # Merge default options with any custom options
    options = {**default_options, **options}
    
    try:
        url, _ = cloudinary_url(image_field.name, **options)
        return url
    except Exception:
        return static('images/placeholder.webp')
