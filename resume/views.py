from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, Textarea
from .forms import PersonalDetailsForm
from .models import Resume, EducationDetails, WorkDetails, Skill
from .utils import render_to_pdf

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        "list_of_resumes": request.user.resume_set.all(),
    }

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def create_view(response):
    resume = Resume(user=response.user)

    if response.method == "POST":
        personal_form       = PersonalDetailsForm(data=response.POST)
        education_formset   = get_education_formset(data=response.POST, instance=resume)
        work_formset        = get_work_experience_formset(data=response.POST, instance=resume)
        skill_formset       = get_skill_formset(data=response.POST, instance=resume)

        if personal_form.is_valid() and education_formset.is_valid() and work_formset.is_valid() and skill_formset.is_valid():
            print("[I] All forms valid. Saving...")

            resume.save()

            personal_details_model = personal_form.save(commit=False)
            personal_details_model.resume = resume
            personal_details_model.save()

            education_formset.save()
            work_formset.save()
            skill_formset.save()

            return redirect('edit/%i' % len(response.user.resume_set.all()))
    else:
        personal_form       = get_personal_form()
        education_formset   = get_education_formset(instance=resume, extra=3)
        work_formset        = get_work_experience_formset(instance=resume, extra=3)
        skill_formset       = get_skill_formset(instance=resume, extra=3)

    context = {
        "personal_form": personal_form,
        "education_formset": education_formset,
        "work_formset": work_formset,
        "skill_formset": skill_formset
    }

    return render(response, 'resume/create.html', context)

@login_required(login_url='login')
def edit_view(response, pk):
    resume = response.user.resume_set.get(pk=pk)

    # Cookie related
    extra_education_cookie_name = ('extra_education_form_pk_%i' % pk)
    extra_education_forms = response.session.get(extra_education_cookie_name)

    extra_work_cookie_name = ('extra_work_form_pk_%i' % pk)
    extra_work_forms = response.session.get(extra_work_cookie_name)

    extra_skill_cookie_name = ('extra_skill_form_pk_%i' % pk)
    extra_skill_forms = response.session.get(extra_skill_cookie_name)

    # Initialise cookies
    if type(extra_education_forms) is not int or extra_education_forms is None:
        response.session[extra_education_cookie_name] = extra_education_forms = 1

    if type(extra_work_forms) is not int or extra_work_forms is None:
        response.session[extra_work_cookie_name] = extra_work_forms = 1

    if type(extra_skill_forms) is not int or extra_skill_forms is None:
        response.session[extra_skill_cookie_name] = extra_skill_forms = 1

    if response.method == "POST":
        personal_form = PersonalDetailsForm(data=response.POST, instance=resume.personaldetails)

        if response.POST.get("new_education"):
            print("[I] User requested extra education form")

            extra_education_forms += 1
            response.session[extra_education_cookie_name] = extra_education_forms

        elif response.POST.get('new_work'):
            print("[I] User requested extra work form")

            extra_work_forms += 1
            response.session[extra_work_cookie_name] = extra_work_forms

        elif response.POST.get('new_skill'):
            print("[I] User requested extra skill form")

            extra_skill_forms += 1
            response.session[extra_work_cookie_name] = extra_skill_forms

        elif response.POST.get('download_pdf'):
            education_formset = get_education_formset(data=response.POST, instance=resume)
            work_formset = get_work_experience_formset(data=response.POST, instance=resume)
            skill_formset = get_skill_formset(data=response.POST, instance=resume)

            context = {
                "personal_form": personal_form,
                "education_formset": education_formset,
                "work_formset": work_formset,
                "skill_formset": skill_formset
            }

            pdf = render_to_pdf('resume/resume_preview.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        else:
            education_formset   = get_education_formset(data=response.POST, instance=resume)
            work_formset        = get_work_experience_formset(data=response.POST, instance=resume)
            skill_formset       = get_skill_formset(data=response.POST, instance=resume)

            if personal_form.is_valid() and education_formset.is_valid() and work_formset.is_valid() and skill_formset.is_valid():
                print("[I] All forms valid. Saving...")

                personal_details_model = personal_form.save(commit=False)
                personal_details_model.resume = resume
                personal_details_model.save()

                education_formset.save()
                work_formset.save()
                skill_formset.save()

        education_formset = get_education_formset(data=response.POST, instance=resume, extra=extra_education_forms)
        work_formset = get_work_experience_formset(data=response.POST, instance=resume, extra=extra_work_forms)
        skill_formset = get_skill_formset(data=response.POST, instance=resume, extra=extra_skill_forms)

    else:
        personal_form       = get_personal_form(resume)
        education_formset   = get_education_formset(instance=resume, extra=extra_education_forms)
        work_formset        = get_work_experience_formset(instance=resume, extra=extra_work_forms)
        skill_formset       = get_skill_formset(instance=resume, extra=extra_skill_forms)

    context = {
        "personal_form": personal_form,
        "education_formset": education_formset,
        "work_formset": work_formset,
        "skill_formset": skill_formset
    }

    return render(response, 'resume/edit.html', context)

def get_personal_form(user_resume_model=None):
    if user_resume_model is None:
        return PersonalDetailsForm()
    else:
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

def get_skill_formset(instance, data=None, extra=0):
    SkillFormset = inlineformset_factory(Resume, Skill, extra=extra, fields=(
        'skill_name',
        'skill_level',
        'description'
    ))

    skill_formset = SkillFormset(data=data, instance=instance)

    # Apply Bootstrap styling
    for skill_form in skill_formset:
        for field in skill_form.fields:
            skill_form.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            if field == 'description':
                skill_form.fields[field].widget = Textarea()
                skill_form.fields[field].widget.attrs.update({
                    'rows': 4
                })

    return skill_formset