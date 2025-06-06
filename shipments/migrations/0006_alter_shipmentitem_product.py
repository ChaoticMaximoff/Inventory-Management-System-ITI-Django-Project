# Generated by Django 5.1.7 on 2025-03-22 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_image'),
        ('shipments', '0005_alter_shipmentitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shipment_items', to='inventory.product'),
        ),
    ]
