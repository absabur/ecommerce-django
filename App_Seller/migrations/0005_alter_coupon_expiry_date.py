# Generated by Django 5.0.1 on 2024-02-11 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Seller', '0004_coupon_expiry_date_coupon_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateField(),
        ),
    ]