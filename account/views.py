from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
def login_view(response):
    if response.method == "POST":
        form = AuthenticationForm(data=response.POST)

        if form.is_valid():
            return redirect('dashboard')

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
            return redirect(LOGIN_REDIRECT_URL)

    else:
        form = UserCreationForm()

    context = {
        "form": form
    }

    return render(response, 'account/register.html', context)