from django.db import models
from django.contrib.auth import get_user_model

from ibs.tools.mixins import BaseMixin
from ibs.users.models import Committee

class Activity(BaseMixin):
  name = models.CharField(max_length=100, verbose_name="Naam")
  description = models.CharField(max_length=1000, verbose_name="Omschrijving")
  date = models.DateField(verbose_name="Datum")
  start_time = models.TimeField(verbose_name="Starttijd")
  location = models.CharField(max_length=100, verbose_name="Locatie")
  organisation = models.ForeignKey(Committee, on_delete=models.SET_NULL, null=True, verbose_name="Organisatie")

  def __str__(self):
    return str(f'{self.name}, {self.location}, {self.organisation.name}, {self.date} {self.start_time}')

  class Meta:
    verbose_name = "Activity"
    verbose_name_plural = "Activities"

class Participant(BaseMixin):
  activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  present = models.BooleanField(verbose_name="Aanwezig")

  def __str__(self):
    p = "aanwezig" if self.present else "afwezig"
    return f'{self.user} is {p} at {self.activity}'

  class Meta:
    verbose_name = "Participant"
    verbose_name_plural = "Participants"