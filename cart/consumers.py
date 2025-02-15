import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from products.models import Product
from .cart import Cart
from asgiref.sync import sync_to_async
# from django.core.cache import cache

class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "cart_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "cart_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        product_id = text_data_json.get('product_id')

        if action == 'check_stock':
            stock = await self.get_product_stock(product_id)
            await self.send(json.dumps({
                'type': 'stock_update',
                'product_id': product_id,
                'stock': stock
            }))
        elif action == 'check_price':
            price_info = await self.get_product_price(product_id)
            await self.send(json.dumps({
                'type': 'price_update',
                'product_id': product_id,
                'price': price_info['price'],
                'sale_price': price_info['sale_price'],
                'on_sale': price_info['on_sale']
            }))

    async def stock_update(self, event):
        await self.send(json.dumps(event))

    async def price_update(self, event):
        await self.send(json.dumps(event))

    async def cart_update(self, event):
        await self.send(json.dumps(event))

    @database_sync_to_async
    def get_product_stock(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            return product.stock
        except Product.DoesNotExist:
            return 0

    @database_sync_to_async
    def get_product_price(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            return {
                'price': str(product.price),
                'sale_price': str(product.sale_price) if product.sale_price else None,
                'on_sale': product.on_sale
            }
        except Product.DoesNotExist:
            return {'price': '0', 'sale_price': None, 'on_sale': False}
