from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from .forms import RegisterForm

# Create your views here.
def login_view(response):
    # No need to login if user
    # is authenticated
    if response.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if response.method == "POST":
        form = AuthenticationForm(data=response.POST)

        if form.is_valid():
            # Log user in
            user = form.get_user()
            login(response, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(response, 'account/login.html', context)

def logout_view(response):
    context = {
        "message": ""
    }

    if response.user.is_authenticated:
        logout(response)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        context['message'] = "You're not logged in why would you logout D:"
        return render(response, 'oops.html', context)

def register_view(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        print(response.POST)

        if form.is_valid():
            form.save()

            # Log user in
            user = form.cleaned_data['email']
            login(response, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = RegisterForm()

    context = {
        "form": form
    }

    return render(response, 'account/register.html', context)