# Generated by Django 4.1.3 on 2022-11-12 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221112_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_bierco',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_colosseum',
        ),
    ]
