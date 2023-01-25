# Generated by Django 4.1.5 on 2023-01-11 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maluspunt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reason', models.CharField(max_length=1024)),
                ('amount', models.IntegerField()),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maluspunten_added_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maluspunten_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Maluspunt',
                'verbose_name_plural': 'Maluspunten',
            },
        ),
    ]