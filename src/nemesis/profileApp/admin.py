from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('address',)}),
    )

admin.site.register(User, MyUserAdmin)