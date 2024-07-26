from django.contrib import admin
from .models import User, Address, UserProfile


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'address1',
        'zipcode',
        'phone',
        'city',
        'country',
        'email',
        'status'
        ]

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

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'profile_image',
        'bio',
        'phone_number',
        'verified',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
