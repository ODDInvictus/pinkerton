from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from ibs.users.managers import UserManager

class Generation(models.Model):
  """
    A generation is a group of users that became aspiring members at the same time.
  """
  name = models.CharField(max_length=100, verbose_name="Naam")
  generation_number = models.IntegerField(verbose_name="Generatie nummer", unique=True)
  start_date = models.DateField(verbose_name="Startdatum")

  class Meta:
    verbose_name = "Generatie"
    verbose_name_plural = "Generaties"
    ordering = ['generation_number']

  def __str__(self):
    return f'Generatie {self.generation_number}: {self.name}'


class User(AbstractUser):
  # override the manager
  objects = UserManager()
  
  # overwriting the AbstractUser class
  first_name = models.CharField(max_length=100, verbose_name="Voornaam")
  last_name = models.CharField(max_length=100, verbose_name="Achternaam")
  email = models.EmailField(verbose_name="E-mailadres")
  username = models.CharField(max_length=100, unique=True, verbose_name="Gebruikersnaam")

  # Base properties
  nickname = models.CharField(max_length=100, verbose_name="Bijnaam", blank=True)
  initials = models.CharField(max_length=10, verbose_name="Initialen", blank=True)
  profile_picture = models.ImageField(upload_to='images/profile_pictures', blank=True)

  # Important dates
  birth_date = models.DateField(null=True, blank=True, verbose_name="Geboortedatum")
  # Fakka niels, deze datums kunnen nu null zijn want ik mag anders geen superuser maken kusjes
  first_drink_invited_at = models.DateField(null=True, verbose_name="Datum van eerste meeborrel")
  became_aspiring_member = models.DateField(null=True, verbose_name="Datum van aspirant-lidmaatschap")
  became_member = models.DateField(null=True, blank=True, verbose_name="Datum van lidmaatschap")

  # Extra properties
  generation = models.ForeignKey(Generation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Generatie")
  bio = models.TextField(max_length=500, blank=True)
  phone_number = models.CharField(max_length=20)
  
  # LDAP
  last_synced = models.DateTimeField(null=True, blank=True, verbose_name="Laatst gesynchroniseerd")
  
  class Meta:
    verbose_name = "Gebruiker"
    verbose_name_plural = "Gebruikers"
    ordering = ['last_name', 'first_name']

  def __str__(self):
    return f'{self.first_name} {self.last_name} ({self.username})'
    
  def get_full_name(self):
    return f'{self.first_name} {self.last_name}'

  def get_committees(self):
    committees = CommitteeMember.objects.filter(user=self, active=True).all()
    return [f.committee for f in committees]

  # Special committee helpers
  def _is_committee(self, abbreviation):
    committees = self.get_committees()
    for committee in committees:
      if committee.abbreviation == abbreviation:
        return True
    return False

  def is_senaat(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_SENATE)

  def is_super_admin(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_ADMINS)

  def is_colosseum(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_COLOSSEUM)

  def is_ict(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_ICT)

  def is_kasco(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_KASCO)

  def is_member(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_MEMBER)

  def is_aspiring_member(self):
    return self._is_committee(settings.COMMITTEE_ABBREVIATION_ASPIRING_MEMBER)


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
  logo = models.ImageField(upload_to='images/committee_logos', blank=True, verbose_name="Commissie logo")
  photo = models.ImageField(upload_to='images/committee_photos', blank=True, verbose_name="Commissie foto")

  class Meta:
    verbose_name = "Commissie"
    verbose_name_plural = "Commissies"
    ordering = ['name']

  def __str__(self):
    return self.name
  
  def get_email(self):
    if self.email:
      return f'{self.name} <{self.email}>'
    return f'{self.name} <{self.abbreviation}@oddinvictus.nl>'

  def get_members(self):
    if not self.active:
      return []
    return CommitteeMember.objects.filter(committee=self, active=True)

  def get_old_members(self):
    if not self.active:
      return []
    return CommitteeMember.objects.filter(committee=self, active=False)

class CommitteeMember(models.Model):
  """
  A user that is in a committee
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruiker")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, verbose_name="Commissie")
  function = models.CharField(max_length=100, verbose_name="Functie")
  note = models.CharField(max_length=1000, blank=True, verbose_name="Notitie")
  begin = models.DateField(verbose_name="Begonnen op", auto_now_add=True)
  end = models.DateField(null=True, blank=True, verbose_name="Gestopt op")
  active = models.BooleanField(default=True, verbose_name="Actief")

  class Meta:
    verbose_name = "Commissie lid"
    verbose_name_plural = "Commissie leden"
    ordering = ['end', '-begin', 'user']

  def __str__(self):
    return f'{self.user.get_full_name()}'
  