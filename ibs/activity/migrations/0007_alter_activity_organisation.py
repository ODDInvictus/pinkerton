# Generated by Django 4.1.3 on 2022-11-13 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_became_aspiring_member_alter_user_email_and_more'),
        ('activity', '0006_rename_person_participant_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.committee', verbose_name='Organisatie'),
        ),
    ]
