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
    resume = response.user.resume_set.get(pk=pk)

    if response.method == "POST":
        # Fill up them lovely forms
        personal_form = PersonalDetailsForm(data=response.POST, instance=resume.personaldetails)
        education_formset = get_education_formset(data=response.POST, instance=resume)

        if personal_form.is_valid() and education_formset.is_valid():
            print("[I] Saving models...")
            personal_details_model = personal_form.save(commit=False)
            personal_details_model.resume = resume
            personal_details_model.save()

            education_formset.save()
        else:
            if not personal_form.is_valid(): print(personal_form.errors)
            if not education_formset.is_valid(): print(education_formset.errors)

    else:
        personal_form = get_personal_form(resume)
        education_formset = get_education_formset(resume)

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

def get_education_formset(instance, data=None, extra=3):
    EducationFormset = inlineformset_factory(Resume, EducationDetails, extra=extra, fields=(
        'institution',
        'course',
        'start_date',
        'end_date',
        'country',
        'description'
    ))

    education_formset = EducationFormset(data=data, instance=instance)

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
