# Generated by Django 4.1.5 on 2023-01-11 20:45

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=100, verbose_name='Voornaam')),
                ('last_name', models.CharField(max_length=100, verbose_name='Achternaam')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mailadres')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Gebruikersnaam')),
                ('nickname', models.CharField(blank=True, max_length=100, verbose_name='Bijnaam')),
                ('initials', models.CharField(blank=True, max_length=10, verbose_name='Initialen')),
                ('profile_picture', models.ImageField(blank=True, upload_to='images/profile_pictures')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Geboortedatum')),
                ('first_drink_invited_at', models.DateField(null=True, verbose_name='Datum van eerste meeborrel')),
                ('became_aspiring_member', models.DateField(null=True, verbose_name='Datum van aspirant-lidmaatschap')),
                ('became_member', models.DateField(blank=True, null=True, verbose_name='Datum van lidmaatschap')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('phone_number', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Gebruiker',
                'verbose_name_plural': 'Gebruikers',
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Naam')),
                ('abbreviation', models.CharField(max_length=10, verbose_name='Afkorting')),
                ('description', models.CharField(max_length=1000, verbose_name='Omschrijving')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Opgericht op')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Laatst bijgewerkt op')),
                ('active', models.BooleanField(default=True, verbose_name='Actief')),
                ('admin_rights', models.BooleanField(default=False, verbose_name='Heeft admin rechten')),
                ('website', models.URLField(blank=True, verbose_name='Commissie website')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Commissie email')),
                ('logo', models.ImageField(blank=True, upload_to='images/committee_logos', verbose_name='Commissie logo')),
                ('photo', models.ImageField(blank=True, upload_to='images/committee_photos', verbose_name='Commissie foto')),
            ],
            options={
                'verbose_name': 'Commissie',
                'verbose_name_plural': 'Commissies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Naam')),
                ('generation_number', models.IntegerField(unique=True, verbose_name='Generatie nummer')),
                ('start_date', models.DateField(verbose_name='Startdatum')),
            ],
            options={
                'verbose_name': 'Generatie',
                'verbose_name_plural': 'Generaties',
                'ordering': ['generation_number'],
            },
        ),
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(max_length=100, verbose_name='Functie')),
                ('note', models.CharField(blank=True, max_length=1000, verbose_name='Notitie')),
                ('begin', models.DateField(auto_now_add=True, verbose_name='Begonnen op')),
                ('end', models.DateField(blank=True, null=True, verbose_name='Gestopt op')),
                ('active', models.BooleanField(default=True, verbose_name='Actief')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.committee', verbose_name='Commissie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Gebruiker')),
            ],
            options={
                'verbose_name': 'Commissie lid',
                'verbose_name_plural': 'Commissie leden',
                'ordering': ['end', '-begin', 'user'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='generation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.generation', verbose_name='Generatie'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
