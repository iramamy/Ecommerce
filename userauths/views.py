from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from .forms import UserRegisterForm
from .models import User



def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        

        if form.is_valid():

            new_user = form.save()
            username = form.cleaned_data['username']

            messages.success(request, f"{username}, your account was created successfully.")

            new_user = auth.authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
                )

            auth.login(request, new_user)

            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'userauths/register.html', context)


def signin(request):

    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in!')

        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                email=email,
            )

            user = auth.authenticate(
            request, 
            email=email, 
            password=password
            )

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('home')

        except User.DoesNotExist:
            messages.error(request, f"User with {email} does not exist!")
            return redirect('signin')

    return render(request, 'userauths/signin.html')


def signout(request):
    auth.logout(request)

    messages.success(request, 'You are currently logged out!')
    return redirect('signin')
