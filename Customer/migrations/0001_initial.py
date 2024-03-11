# Generated by Django 4.2 on 2024-03-11 06:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_number', models.IntegerField()),
                ('delivery_option', models.CharField(choices=[('road', 'By Road'), ('air', 'By Air'), ('sea', 'By Sea')], max_length=10)),
                ('delivery_type', models.CharField(choices=[('normal', 'Normal'), ('speed', 'Speed')], max_length=10)),
                ('pickup_date', models.DateField(blank=True, null=True)),
                ('pickup_time', models.TimeField(blank=True, null=True)),
                ('package_weight', models.DecimalField(blank=True, decimal_places=5, max_digits=5, null=True)),
                ('number_of_packages', models.IntegerField(blank=True, null=True)),
                ('sender_name', models.CharField(blank=True, max_length=254, null=True)),
                ('sender_address', models.TextField(blank=True, null=True)),
                ('sender_city', models.CharField(blank=True, max_length=254, null=True)),
                ('sender_pincode', models.IntegerField(blank=True, null=True)),
                ('sender_state', models.CharField(blank=True, max_length=254, null=True)),
                ('sender_country', models.CharField(blank=True, max_length=254, null=True)),
                ('sender_contact_no', models.IntegerField(blank=True, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=254, null=True)),
                ('receiver_address', models.TextField(blank=True, null=True)),
                ('receiver_city', models.CharField(blank=True, max_length=254, null=True)),
                ('receiver_pincode', models.IntegerField(blank=True, null=True)),
                ('receiver_state', models.CharField(blank=True, max_length=254, null=True)),
                ('receiver_country', models.CharField(blank=True, max_length=254, null=True)),
                ('receiver_contact_no', models.IntegerField(blank=True, null=True)),
                ('is_confirmed', models.BooleanField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(blank=True, default=0, null=True)),
            ],
        ),
    ]
