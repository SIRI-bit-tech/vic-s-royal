from .models import Category

def categories(request):
    """Add active categories to all templates' context"""
    return {
        'categories': Category.objects.filter(active=True)
    }