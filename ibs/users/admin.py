from django.contrib import admin
from django.contrib.auth.models import Group

from ibs.users.models import User, Generation, Committee, Function

# Register your models here.

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Generation)
admin.site.register(Committee)
admin.site.register(Function)