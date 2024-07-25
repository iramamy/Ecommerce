from django import forms
from userauths.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'user',
            'first_name',
            'last_name',
            'address1',
            'address2',
            'zipcode',
            'phone',
            'city',
            'country',
            'email',
        ]

