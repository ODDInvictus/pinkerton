from django.contrib import admin

from .models import Activity, Participant

# Register your models here.

admin.site.register(Activity)
admin.site.register(Participant)