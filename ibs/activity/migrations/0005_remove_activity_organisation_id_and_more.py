# Generated by Django 4.1.3 on 2022-11-12 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_participant_delete_peoplepresent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='organisation_id',
        ),
        migrations.AddField(
            model_name='activity',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.committee', verbose_name='Organisatie'),
        ),
    ]
