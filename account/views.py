from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
def login_view(request):
    context = {}

    return render(request, 'account/login.html', context)

def register_view(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()

    else:
        form = RegisterForm()

    context = {
        "form": form
    }

    return render(response, 'account/register.html', context)