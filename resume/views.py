from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, Textarea
from .forms import PersonalDetailsForm
from .models import Resume, EducationDetails

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        "list_of_resumes": request.user.resume_set.all(),
    }

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def edit_vew(response, pk):
    # Let's start by defining $resume and $personal_details
    # first since we are only editing one $resume and a time
    # and $resume has a one-to-one relation with $personal_details.
    resume = response.user.resume_set.get(pk=pk)

    if response.method == "POST":
        if response.POST.get("new_education"):
            pass
    else:
        personal_form = get_personal_form(resume)

        education_formset = get_education_formset(resume, extra=0)

    context = {
        "personal_form": personal_form,
        "education_formset": education_formset,
    }

    return render(response, 'resume/create.html', context)

def get_personal_form(user_resume_model):
    personal_details = user_resume_model.personaldetails

    return PersonalDetailsForm(initial={
        'first_name': personal_details.first_name,
        'last_name': personal_details.last_name,
        'email_address': personal_details.email_address,
        'phone': personal_details.phone,
        'about_me': personal_details.about_me,
    })

def get_education_formset(user_resume_model, extra):
    EducationFormset = inlineformset_factory(Resume, EducationDetails, extra=extra, fields=(
        'institution',
        'course',
        'start_date',
        'end_date',
        'country',
        'description'
    ))

    education_formset = EducationFormset(instance=user_resume_model)

    # Somehow crispy tags aren't applying
    # Bootstrap styling onto the inline
    # form so this is a workaround :/
    for education_form in education_formset:
        for field in education_form.fields:
            education_form.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            if field == 'description':
                education_form.fields[field].widget = Textarea()
                education_form.fields[field].widget.attrs.update({
                    'rows': 4
                })

    return education_formset
