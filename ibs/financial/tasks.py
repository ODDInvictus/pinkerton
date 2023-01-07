from django.conf import settings
from datetime import datetime

from ibs.users.models import User, CommitteeMember, Committee
from ibs.financial.models import ContributionTransaction

from ..celery import app

@app.task()
def collect_monthly_contribution():
  """
  Collect monthly contribution from all the members
  """
  print('Collecting monthly contribution')

  member_committee = Committee.objects.filter(abbreviation=settings.COMMITTEE_ABBREVIATION_MEMBER).first()
  member_functions = CommitteeMember.objects.filter(committee=member_committee).all()
  members = User.objects.filter(function__in=member_functions).all()

  added_by = User.objects.get(username=settings.DEFAULT_IBS_USER_USERNAME)

  today = datetime.now()

  for member in members:
    tr = ContributionTransaction(
      user=member,
      date=today,
      description=f'Maandelijke contributie van maand: {today.month}',
      added_by=added_by,
      amount=settings.MONTHLY_CONTRIBUTION)

    tr.save()


@app.task()
def test():
  print('test')