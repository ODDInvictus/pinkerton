from django.contrib.auth.models import AbstractUser
from django.db import models

class Generation(models.Model):
  """
    A generation is a group of users that became aspiring members at the same time.
  """
  name = models.CharField(max_length=100, verbose_name="Naam")
  generation_number = models.IntegerField(verbose_name="Generatie nummer")
  start_date = models.DateField(verbose_name="Startdatum")

  class Meta:
    verbose_name = "Generation"
    verbose_name_plural = "Generations"
    ordering = ['generation_number']

  def __str__(self):
    return f'Generatie {self.generation_number}: {self.name}'


class User(AbstractUser):
  # Base properties
  initials = models.CharField(max_length=10, verbose_name="Initialen", blank=True)
  profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

  # Important dates
  birth_date = models.DateField(null=True, blank=True, verbose_name="Geboortedatum")
  first_drink_invited_at = models.DateField(null=True, blank=True ,verbose_name="Datum van eerste meeborrel")
  became_aspiring_member = models.DateField(null=True, blank=True, verbose_name="Datum van aspirant-lidmaatschap")
  became_member = models.DateField(null=True, blank=True, verbose_name="Datum van lidmaatschap")

  # TODO add last_event_attended

  # Extra properties
  generation = models.ForeignKey(Generation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Generatie")
  bio = models.TextField(max_length=500, blank=True)
  phone_number = models.CharField(max_length=20, blank=True)
  
  # Important committees
  is_senate = models.BooleanField(default=False)
  is_colosseum = models.BooleanField(default=False)
  is_bierco = models.BooleanField(default=False)

  class Meta:
    verbose_name = "User"
    verbose_name_plural = "Users"
    ordering = ['last_name', 'first_name']

  def __str__(self):
    return f'{self.first_name} {self.last_name} ({self.username})'
    
  def get_full_name(self):
    return f'{self.first_name} {self.last_name}'

  def is_senate(self):
    # TODO
    return self.function_set


class Committee(models.Model):
  name = models.CharField(max_length=100, verbose_name="Naam")
  abbreviation = models.CharField(max_length=10, verbose_name="Afkorting")
  description = models.CharField(max_length=1000, verbose_name="Omschrijving")
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Opgericht op")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Laatst bijgewerkt op")

  active = models.BooleanField(default=True, verbose_name="Actief")
  admin_rights = models.BooleanField(default=False, verbose_name="Heeft admin rechten")

  website = models.URLField(blank=True, verbose_name="Commissie website")
  email = models.EmailField(blank=True, verbose_name="Commissie email")
  logo = models.ImageField(upload_to='committee_logos', blank=True, verbose_name="Commissie logo")
  photo = models.ImageField(upload_to='committee_photos', blank=True, verbose_name="Commissie foto")

  class Meta:
    verbose_name = "Committee"
    verbose_name_plural = "Committees"
    ordering = ['name']

  def __str__(self):
    return self.name

  def get_members(self):
    if not self.active:
      return []
    # TODO


class Function(models.Model):
  """
  Function of a committee member
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruiker")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, verbose_name="Commissie")
  function = models.CharField(max_length=100, verbose_name="Functie")
  note = models.CharField(max_length=1000, blank=True, verbose_name="Notitie")
  begin = models.DateField(verbose_name="Begonnen op")
  end = models.DateField(null=True, blank=True, verbose_name="Gestopt op")
  active = models.BooleanField(default=True, verbose_name="Actief")

  class Meta:
    verbose_name = "Function"
    verbose_name_plural = "Functions"
    ordering = ['end', '-begin', 'user']

  def __str__(self):
    active = 'Actief' if self.active else 'Niet actief'
    return f'{self.user} is {self.function} in {self.function} ({active})'

  