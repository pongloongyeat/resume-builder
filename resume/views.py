from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, Textarea
from .forms import PersonalDetailsForm
from .models import Resume, EducationDetails, WorkDetails

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
    extra_education_cookie_name = 'extra_education_form_pk_%i'
    extra_education_forms = response.session.get(extra_education_cookie_name)

    # Initialise extra_education_cookie
    if type(extra_education_forms) is not int or extra_education_forms is None:
        response.session[extra_education_cookie_name] = extra_education_forms = 1

    if response.method == "POST":
        personal_form = PersonalDetailsForm(data=response.POST, instance=resume.personaldetails)

        if response.POST.get("new_education"):
            print("[I] User requested extra education form")

            extra_education_forms += 1
            response.session[extra_education_cookie_name] = extra_education_forms
            education_formset = get_education_formset(data=response.POST, instance=resume, extra=4)
        else:
            education_formset = get_education_formset(data=response.POST, instance=resume)

        if personal_form.is_valid() and education_formset.is_valid():
            personal_details_model = personal_form.save(commit=False)
            personal_details_model.resume = resume
            personal_details_model.save()

            education_formset.save()
    else:
        personal_form = get_personal_form(resume)
        education_formset = get_education_formset(resume, extra=extra_education_forms)

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

def get_education_formset(instance, data=None, extra=0):
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

def get_work_experience_formset(instance, data=None, extra=0):
    WorkFormset = inlineformset_factory(Resume, WorkDetails, extra=extra, fields=(
        'position',
        'company_name',
        'start_date',
        'end_date',
        'country',
        'description'
    ))

    work_formset = WorkFormset(data=data, instance=instance)

    # Apply Bootstrap styling
    for work_form in work_formset:
        for field in work_form.fields:
            work_form.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            if field == 'description':
                work_form.fields[field].widget = Textarea()
                work_form.fields[field].widget.attrs.update({
                    'rows': 4
                })

    return work_formset