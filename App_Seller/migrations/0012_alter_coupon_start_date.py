# Generated by Django 5.0.1 on 2024-02-12 07:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Seller', '0011_alter_coupon_start_date_order_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 13, 51, 0, 518524)),
        ),
    ]