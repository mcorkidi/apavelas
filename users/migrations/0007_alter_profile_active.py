# Generated by Django 4.1 on 2022-08-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
