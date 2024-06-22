# Generated by Django 4.2 on 2024-06-21 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0017_orderqueries_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmenttracking',
            name='delivery_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='delivery_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='destination_hub_arrival_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='is_arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='return_processed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='return_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='shipped_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shipmenttracking',
            name='status_history',
            field=models.JSONField(blank=True, default=list),
        ),
    ]