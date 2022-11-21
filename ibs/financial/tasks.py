from django.conf import settings
from datetime import datetime

from ibs.users.models import User, CommitteeMember, Committee
from ibs.financial.models import ContributionTransaction

from celery import shared_task

@shared_task()
def collect_monthly_contribution():
  """
  Collect monthly contribution from all the members
  """
  member_committee = Committee.objects.filter(abbreviation=settings.COMMITTEE_ABBREVIATION_MEMBER).first()
  member_functions = CommitteeMember.objects.filter(committee=member_committee).all()
  members = User.objects.filter(function__in=member_functions).all()

  today = datetime.now()

  for member in members:
    tr = ContributionTransaction(
      user=member,
      date=today,
      description=f'Maandelijke contributie van maand: {today.month}',
      amount=settings.MONTHLY_CONTRIBUTION)

    tr.save()