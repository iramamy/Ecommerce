from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'updated_at'
        ]

    list_display_links = [
        'username',
        'email'
    ]

admin.site.register(User, UserAdmin)
