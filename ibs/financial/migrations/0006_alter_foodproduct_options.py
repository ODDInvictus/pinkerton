# Generated by Django 4.1.3 on 2022-11-27 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0005_delete_alcoholsaletransaction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodproduct',
            options={'verbose_name': 'Voedingsmiddel', 'verbose_name_plural': 'Voeidingsmiddelen'},
        ),
    ]