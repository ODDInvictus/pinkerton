from datetime import datetime

from django.conf import settings

from .models import Strafbak
from ibs.users.models import User

from ..celery import app

@app.task()
def double_strafbakken():
  """
  Double the amount of strafbakken
  """
  # TODO
  print('TODO')