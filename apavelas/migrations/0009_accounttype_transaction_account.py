# Generated by Django 4.1 on 2022-09-22 23:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apavelas', '0008_photo_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('debit', models.FloatField(default=0.0)),
                ('credit', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apavelas.accounttype')),
            ],
        ),
    ]
