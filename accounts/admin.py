from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OneTimePassword


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'birth_date', 'organization', 'scientific_degree', 'additional_info')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_reviewer')}
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_reviewer'),
        }),
    )
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_reviewer')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword)
