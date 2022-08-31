# Generated by Django 4.1 on 2022-08-26 05:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_faceimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='memberSince',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='profile',
            name='validTo',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
