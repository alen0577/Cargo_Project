# Generated by Django 4.2 on 2024-04-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Login', '0004_cargoteam_address_cargoteam_city_cargoteam_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargoteam',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='image/profile_picture'),
        ),
    ]
