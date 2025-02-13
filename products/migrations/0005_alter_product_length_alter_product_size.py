# Generated by Django 5.1.4 on 2025-01-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_product_featured_product_meta_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="length",
            field=models.CharField(
                choices=[("short", "Short"), ("medium", "Medium"), ("none", "None")],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="size",
            field=models.CharField(
                choices=[
                    ("S", "Small"),
                    ("M", "Medium"),
                    ("L", "Large"),
                    ("N", "None"),
                ],
                default="M",
                max_length=1,
            ),
        ),
    ]
