# Generated by Django 4.1.3 on 2022-11-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20221112_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, verbose_name='Bijnaam'),
        ),
    ]
