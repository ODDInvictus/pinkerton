from django import forms
from django.conf import settings

from ibs.users.models import User, CommitteeMember

class MaluspuntForm(forms.Form):
  feuten = CommitteeMember.objects.filter(committee__abbreviation=settings.COMMITTEE_ABBREVIATION_ASPIRING_MEMBER)
  members = CommitteeMember.objects.filter(committee__abbreviation=settings.COMMITTEE_ABBREVIATION_MEMBER)
  user = forms.ChoiceField(
    label='Feut',
    choices=[(x.user.id, x.user.get_full_name()) for x in feuten])
  added_by = forms.ChoiceField(
    label='Toegevoegd door',
    choices=[(x.user.id, x.user.get_full_name()) for x in members])
  reason = forms.CharField(max_length=1024, label='Reden')
  amount = forms.IntegerField(label='Aantal maluspunten', initial=1)
  
  