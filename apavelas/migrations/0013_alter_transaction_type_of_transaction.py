# Generated by Django 4.1 on 2022-09-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apavelas', '0012_account_transaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type_of_transaction',
            field=models.CharField(choices=[('INGRESO', 'INGRESO'), ('GASTO', 'GASTO')], default='INGRESO', max_length=7),
        ),
    ]