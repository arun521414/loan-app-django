# Generated by Django 4.0 on 2022-07-28 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_eligibility_profile_eligibile_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='eligibile',
            new_name='eligible',
        ),
    ]
