# Generated by Django 4.1.5 on 2023-01-22 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chugs", "0003_strafbak_date_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="strafbak",
            name="reason",
            field=models.CharField(
                default="Geen reden gegeven", max_length=512, verbose_name="Reden"
            ),
        ),
    ]
