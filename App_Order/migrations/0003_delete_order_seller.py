# Generated by Django 5.0.1 on 2024-02-12 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Order', '0002_order_seller'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order_seller',
        ),
    ]
