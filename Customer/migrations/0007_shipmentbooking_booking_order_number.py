# Generated by Django 4.2 on 2024-03-15 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_rename_tracking_code_shipmentbooking_uid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentbooking',
            name='booking_order_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
