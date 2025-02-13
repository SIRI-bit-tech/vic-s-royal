from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_populate_invoice_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='invoice_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

