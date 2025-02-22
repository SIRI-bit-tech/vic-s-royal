# Generated by Django 5.1.4 on 2025-02-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_length_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='categories/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.PositiveIntegerField(blank=True, help_text='Discount percentage (0-100)', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='on_sale',
            field=models.BooleanField(default=False, help_text='Check to put this product on sale'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Sale price in Naira (₦)', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['on_sale'], name='products_pr_on_sale_35aa59_idx'),
        ),
    ]
