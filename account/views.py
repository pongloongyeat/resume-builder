from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings

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

def register_view(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)

        if form.is_valid():
            # Log user in
            user = form.get_user()
            login(response, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = UserCreationForm()

    context = {
        "form": form
    }

    return render(response, 'account/register.html', context)