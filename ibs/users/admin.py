from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group
from ibs.users.forms import IBSUserChangeForm, IBSUserCreationForm

from ibs.users.models import User, Generation, Committee, CommitteeMember

# Register your models here.

class IBSUserAdmin(UserAdmin):
  add_form = IBSUserCreationForm
  form = IBSUserChangeForm
  model = User

  list_display = ('username', 'nickname', 'email', 'is_senaat', 'is_member')

  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {
      'fields': (
        'first_name', 
        'last_name', 
        'initials', 
        'nickname', 
        'email', 
        'phone_number', 
        'profile_picture', 
        'bio', 
        'birth_date', 
        'first_drink_invited_at', 
        'became_aspiring_member', 
        'became_member', 
        'generation')}),
      ('Permissions', {
        'fields': (
          'is_active',
          'is_staff',
          'is_superuser',
          'groups',
          'user_permissions')}),
      ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
        'fields': (
          'first_name',
          'last_name',
          'email', 
          'username',
          'password1', 
          'password2', 
          'is_staff', 
          'is_active')}
      ),
    )
  

admin.site.unregister(Group)
admin.site.register(Generation)
admin.site.register(Committee)
admin.site.register(CommitteeMember)
admin.site.register(User, IBSUserAdmin)

admin.site.register(Session)