from django.contrib import messages
from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.warning(request, 'You are not allowed to access this page!')

            return redirect('signin')

        return view_func(request, *args, **kwargs)

    return wrapper