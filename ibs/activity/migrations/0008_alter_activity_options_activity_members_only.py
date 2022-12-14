# Generated by Django 4.1.3 on 2022-11-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_alter_activity_organisation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activiteit', 'verbose_name_plural': 'Activiteiten'},
        ),
        migrations.AddField(
            model_name='activity',
            name='members_only',
            field=models.BooleanField(default=False, verbose_name='Alleen voor leden'),
        ),
    ]
