# Generated by Django 4.1 on 2022-09-09 19:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apavelas', '0006_remove_photo_user_id_photo_uploader_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]