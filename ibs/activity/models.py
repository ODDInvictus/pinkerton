from django.db import models
from django.contrib.auth import get_user_model
from ibs.tools.mixins import BaseMixin

class Activity(BaseMixin):
  name = models.CharField(max_length=100, verbose_name="Naam")
  description = models.CharField(max_length=1000, verbose_name="Omschrijving")
  date = models.DateField(verbose_name="Datum")
  start_time = models.TimeField(verbose_name="Starttijd")
  location = models.CharField(max_length=100, verbose_name="Locatie")
  organisation_id = models.IntegerField(verbose_name="Organisatie")

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Activity"
    verbose_name_plural = "Activities"

class Participant(BaseMixin):
  activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
  person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  present = models.BooleanField(verbose_name="Aanwezig")

  def __str__(self):
    return self.activity_id

  class Meta:
    verbose_name = "Participant"
    verbose_name_plural = "Participants"