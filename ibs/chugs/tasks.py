from celery import shared_task
from datetime import datetime

from django.conf import settings

from .models import Strafbak
from ibs.users.models import User

@shared_task()
def double_strafbakken():
  """
  Double the amount of strafbakken
  """
  # TODO: Verdubbel eerst het aantal strafbakken, indien het negatief is, haal dan de min weg :)))

  date = datetime.now()
  reason = f'Verdubbeling van strafbakken {date.month}-{date.year}'
  giver = User.objects.get(username=settings.DEFAULT_IBS_USER_USERNAME)

  # First, get the amount of strafbakken
  bak_per_receiver = {}
  for strafbak in Strafbak.objects.filter(used=False).all():
    if strafbak.receiver in bak_per_receiver:
      bak_per_receiver[strafbak.receiver] += 1
    else:
      bak_per_receiver[strafbak.receiver] = 1

  for receiver, amount in bak_per_receiver.items():
    if amount <= 0:
      continue

    for i in range(amount):
      bak = Strafbak.objects.create(receiver=receiver, giver=giver, reason=reason + f' {i+1}/{amount}')
      bak.save()