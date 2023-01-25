# Generated by Django 4.1.5 on 2023-01-11 20:46
from django.conf import settings
from django.db import migrations

def make_ibs_user(apps, schema_editor):
    IbsUser = apps.get_model('users', 'User')
    Generartion = apps.get_model('users', 'Generation')

    gen = Generartion.objects.get_or_create(
        name="Bots",
        generation_number=-1,
        start_date='2021-09-07'
    )
    
    gen = gen[0]
    
    username = settings.DEFAULT_IBS_USER_USERNAME
    email = settings.DEFAULT_IBS_USER_EMAIL
    
    IbsUser.objects.filter(username=username).delete()

    user = IbsUser.objects.create_user(
        username, 
        email,
        first_name='Invictus',
        last_name='Bier Systeem',
        birth_date='2021-09-07',
        first_drink_invited_at='2021-09-07',
        became_aspiring_member='2021-09-07',
        generation=gen,
        bio='Account voor automagische IBS dingetjes',
        phone_number='0612345678',
    )

    user.active = False

    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_ibs_user),
    ]