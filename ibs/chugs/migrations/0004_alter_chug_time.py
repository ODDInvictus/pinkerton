# Generated by Django 4.1.3 on 2022-11-27 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chugs', '0003_alter_strafbak_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chug',
            name='time',
            field=models.TimeField(auto_now_add=True, verbose_name='Tijdstip'),
        ),
    ]