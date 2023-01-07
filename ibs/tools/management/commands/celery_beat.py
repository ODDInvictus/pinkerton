import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
  celery_beat_cmd = "celery -A ibs worker -B --loglevel=info"
  cmd = f'pkill -f "{celery_beat_cmd}"'
  if sys.platform == "win32":
    cmd = "taskkill /f /t /im celery.exe"

  subprocess.call(shlex.split(cmd))
  subprocess.call(shlex.split(celery_beat_cmd))


class Command(BaseCommand):

  def handle(self, *args, **options):
    print("Starting celery beat worker with autoreload...")
    autoreload.run_with_reloader(restart_celery)