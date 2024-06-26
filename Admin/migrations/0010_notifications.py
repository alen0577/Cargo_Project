# Generated by Django 4.2 on 2024-06-29 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0009_remove_city_country_remove_city_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('date_read', models.DateField(blank=True, null=True)),
                ('time_read', models.TimeField(blank=True, null=True)),
                ('notification_type', models.CharField(choices=[('info', 'Information'), ('warning', 'Warning'), ('error', 'Error'), ('success', 'Success')], default='info', max_length=10)),
                ('recipient_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Admin.city')),
            ],
        ),
    ]
