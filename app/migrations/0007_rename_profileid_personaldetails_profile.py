# Generated by Django 4.0 on 2022-07-25 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_personaldetails_address_personaldetails_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personaldetails',
            old_name='profileId',
            new_name='profile',
        ),
    ]
