from django.db import models

from ibs.users.models import User


# I'm not even going to try to translate that one
class Strafbak(models.Model):
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ontvanger', related_name='stafbak_receiver')
  giver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Gever', related_name='strafbak_giver')
  reason = models.CharField(null=True, max_length=512, verbose_name='Reden')
  date = models.DateTimeField(auto_now_add=True, verbose_name='Datum')
  active = models.BooleanField(default=True, verbose_name='Actief')

  class Meta:
    verbose_name = 'Strafbak'
    verbose_name_plural = 'Strafbakken'

  def __str__(self):
    return f'Strafbak voor {self.receiver} van {self.giver} wegens {self.reason}'


class Anytimer(models.Model):
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ontvanger', related_name='anytimer_receiver')
  giver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Gever', related_name='anytimer_giver')
  reason = models.CharField(max_length=512, verbose_name='Reden')

  class Meta:
    verbose_name = 'Anytimer'
    verbose_name_plural = 'Anytimers'

  def __str__(self):
    return f'Anytimer voor {self.receiver} van {self.giver} wegens {self.reason}'


class Chug(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Gebruiker')
  date = models.DateField(auto_now_add=True, verbose_name='Datum')
  time = models.TimeField(auto_now_add=True, verbose_name='Tijdstip')

  class Meta:
    verbose_name = 'Chug'
    verbose_name_plural = 'Chugs'

  def __str__(self):
    return f'{self.user.get_full_name()} trok een bak op {self.date} om {self.time}'