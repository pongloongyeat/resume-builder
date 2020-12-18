from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {}

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def create_view(response):
    if response.method == "POST":
        personal_form = PersonalDetailsForm(data=response.POST)

        if personal_form.is_valid():
            print(personal_form.cleaned_data['first_name'])
            pass

    else:
        personal_form = PersonalDetailsForm

    context = {
        "personal_form": personal_form
    }

    return render(response, 'resume/create.html', context)