from django.shortcuts import render
import json
from django.http import JsonResponse

from .models import ContactUs

def contact_us(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        contact_data = ContactUs()
        contact_data.first_name = data['name']
        contact_data.email = data['email']
        contact_data.phone = data['telephone']
        contact_data.subject = data['subject']
        contact_data.message = data['message']

        contact_data.save()

        context = {
            'bool': True
        }

        return JsonResponse({
            'data': context
        })

    return render(request, 'contact/contact_us.html')
