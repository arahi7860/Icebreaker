# Generated by Django 4.2.1 on 2023-05-31 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icebreakergen', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]
