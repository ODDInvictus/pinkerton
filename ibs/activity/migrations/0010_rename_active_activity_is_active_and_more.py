# Generated by Django 4.1.4 on 2023-01-04 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_alter_participant_options_activity_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='active',
            new_name='is_active',
        ),
    ]