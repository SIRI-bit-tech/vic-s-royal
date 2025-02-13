from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Resets and recreates all categories with correct slugs'

    def handle(self, *args, **kwargs):
        # First, delete all existing categories
        Category.objects.all().delete()
        
        # Create new categories
        categories = [
            'hair_care_products',
            'hair_extensions',
            'styling_tools',
            'wigs',
        ]
        
        for category_name in categories:
            Category.objects.create(name=category_name)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category: {category_name}')
            )

