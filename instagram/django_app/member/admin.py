from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import MyUser


# Register your models here.

class MyUserAdmin(UserAdmin):
    # pass
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'gender', 'nickname')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    list_display = ('username', 'nickname',)
    list_filter = ('is_staff',)


admin.site.register(MyUser, MyUserAdmin)
