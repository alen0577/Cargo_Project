# Generated by Django 4.2 on 2024-04-04 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_jobapplications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapplications',
            old_name='is_selected',
            new_name='is_shortlisted',
        ),
    ]
