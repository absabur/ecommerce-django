# Generated by Django 5.0.1 on 2024-02-12 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Seller', '0012_alter_coupon_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 20, 1, 59, 523836)),
        ),
    ]