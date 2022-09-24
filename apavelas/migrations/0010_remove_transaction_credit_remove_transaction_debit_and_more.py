# Generated by Django 4.1 on 2022-09-23 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apavelas', '0009_accounttype_transaction_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='debit',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apavelas.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apavelas.accounttype')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='bank',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='apavelas.bank'),
            preserve_default=False,
        ),
    ]
