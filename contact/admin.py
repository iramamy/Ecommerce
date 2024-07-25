from django.contrib import admin
from .models import ContactUs

class ContactUsAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['first_name', 'email', 'phone', 'subject', 'message']

admin.site.register(ContactUs, ContactUsAdmin)
