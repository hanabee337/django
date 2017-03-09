from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from member.models import MyUser


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'img_profile')}),
        ( ('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        ( ('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ( ('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(MyUser, MyUserAdmin)
