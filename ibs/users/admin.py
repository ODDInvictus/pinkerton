from django.contrib import admin

from ibs.users.models import User, Generation, Committee, Function

# Register your models here.

admin.register(User)
admin.register(Generation)
admin.register(Committee)
admin.register(Function)