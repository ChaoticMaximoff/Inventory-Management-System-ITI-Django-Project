from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role',)}),
admin.site.register(User, UserAdmin)