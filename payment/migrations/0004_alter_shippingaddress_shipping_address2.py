# Generated by Django 4.2.17 on 2025-03-01 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_address2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
