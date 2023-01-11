from django.db import models

from ibs.tools.mixins import BaseMixin
from ibs.users.models import User

class Maluspunt(BaseMixin):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maluspunten_user')
  added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maluspunten_added_by'	)
  reason = models.CharField(max_length=1024)
  amount = models.IntegerField()
  
  def __str__(self):
    return f'{self.user.first_name} - {self.reason} - {self.amount}'
  
  class Meta:
    verbose_name = 'Maluspunt'
    verbose_name_plural = 'Maluspunten'