from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Sets up initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            'hair_extensions',
            'wigs',
            'hair_care_products',
            'styling_tools',
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        self.stdout.write(self.style.SUCCESS('Successfully set up categories'))

