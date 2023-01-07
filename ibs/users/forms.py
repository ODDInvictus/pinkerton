from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class IBSUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm):
    model = User
    fields = ('email',)


class IBSUserChangeForm(UserChangeForm):

  class Meta:
    model = User
    fields = ('email',)