from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PersonalDetailsForm, EducationForm
from .models import EducationDetails

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        "list_of_resumes": request.user.resume_set.all(),
    }

    return render(request, 'resume/dashboard.html', context)

@login_required(login_url='login')
def edit_vew(response, id):
    # Let's start by defining $resume and $personal_details
    # first since we are only editing one $resume and a time
    # and $resume has a one-to-one relation with $personal_details.
    resume = response.user.resume_set.get(id=id)
    personal_details = resume.personaldetails
    education_details_all = resume.educationdetails_set.all()

    number_of_education_forms = len(education_details_all)

    if response.method == "POST":
        if response.POST.get("new_education"):
            pass
    else:
        personal_form = PersonalDetailsForm(initial={
            'first_name': personal_details.first_name,
            'last_name': personal_details.last_name,
            'email_address': personal_details.email_address,
            'phone': personal_details.phone,
            'about_me': personal_details.about_me,
        })

        education_forms = [EducationForm(initial={
            'institution': education_details_all[i].institution,
            'course': education_details_all[i].course,
            'start_date': education_details_all[i].start_date,
            'end_date': education_details_all[i].end_date,
            'country': education_details_all[i].country,
        }) for i in range(0, number_of_education_forms)]

    context = {
        "personal_form": personal_form,
        "education_forms": education_forms,
    }

    return render(response, 'resume/create.html', context)

def fill_education_form_list(data, count):
    education_forms = []

    institution_list    = data.getlist('institution')
    course_list         = data.getlist('course')
    start_date_0_list   = data.getlist('start_date_0')
    start_date_1_list   = data.getlist('start_date_1')
    end_date_0_list     = data.getlist('end_date_0')
    end_date_1_list     = data.getlist('end_date_1')
    country_list        = data.getlist('country')

    for i in range(0, count):
        data = {
            'institution': institution_list[i],
            'course': course_list[i],
            'start_date_0': start_date_0_list[i],
            'start_date_1': start_date_1_list[i],
            'end_date_0': end_date_0_list[i],
            'end_date_1': end_date_1_list[i],
            'country': country_list[i]
        }

        education_forms.append(EducationForm(data))

    return education_forms