# Generated by Django 4.1.3 on 2022-11-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_became_aspiring_member_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='became_aspiring_member',
            field=models.DateField(null=True, verbose_name='Datum van aspirant-lidmaatschap'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_drink_invited_at',
            field=models.DateField(null=True, verbose_name='Datum van eerste meeborrel'),
        ),
    ]
