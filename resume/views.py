from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm, EducationForm

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {}

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def create_view(response):
    if response.method == "POST":
        personal_form = PersonalDetailsForm(data=response.POST)
        education_form = EducationForm(data=response.POST)

        if personal_form.is_valid() and education_form.is_valid():
            pass

    else:
        personal_form = PersonalDetailsForm
        education_form = EducationForm

    context = {
        "personal_form": personal_form,
        "education_form": education_form
    }

    return render(response, 'resume/create.html', context)