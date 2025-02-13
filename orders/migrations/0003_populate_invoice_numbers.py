from django.db import migrations
import uuid

def generate_invoice_number(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    for order in Order.objects.all():
        order.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_options_order_invoice_number_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_invoice_number),
    ]

