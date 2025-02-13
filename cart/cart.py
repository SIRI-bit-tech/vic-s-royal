from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            price = product.sale_price if product.on_sale and product.sale_price else product.price
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def decrease(self, product):
        """Decrease the quantity of a product in the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def save(self):
        """Mark session as modified to make sure it gets saved."""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            price = Decimal(item['price'])
            item['price'] = str(price)
            item['total_price'] = str(price * item['quantity'])
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total price of items in cart."""
        total = Decimal('0')
        for item_id, item in self.cart.items():
            total += Decimal(item['price']) * item['quantity']
        return str(total)

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_discount(self):
        """Calculate total discount amount."""
        total_discount = Decimal('0')
        for item_id, item_data in self.cart.items():
            product = Product.objects.get(id=item_id)
            if product.on_sale and product.sale_price:
                discount = (product.price - product.sale_price) * item_data['quantity']
                total_discount += discount
        return str(total_discount)

    def get_total_quantity(self):
        """Get the total quantity of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_item_quantity(self, product_id):
        """Get the quantity of a specific item in the cart."""
        return self.cart.get(str(product_id), {}).get('quantity', 0)

    def get_item_total(self, product_id):
        """Get the total price of a specific item in the cart."""
        item = self.cart.get(str(product_id))
        if item:
            return str(Decimal(item['price']) * item['quantity'])
        return '0'

