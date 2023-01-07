# Generated by Django 4.1.5 on 2023-01-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0007_saletransaction_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Verwijderd'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='settled',
            field=models.BooleanField(default=False, verbose_name='Betaald'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(verbose_name='Datum'),
        ),
    ]
