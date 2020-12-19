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
    id = response.user.id - 1
    collapse_id = len(response.user.resume_set.all()[id].educationdetails_set.all())
    education_forms = []

    if response.method == "POST":
        personal_form = PersonalDetailsForm(data=response.POST)

        # Since we have multiple same forms in one page,
        # we'll have to parse it through a custom function
        # since I don't know of any way Django can process
        # lists of data.
        education_forms = fill_education_form_list(response.POST, collapse_id)

        # A valid flag removes the need of going through
        # each form list and checking if all are valid.
        valid_flag = True

        if personal_form.is_valid() is False:
            valid_flag = False
        else:
            # Personal is valid, we just have to check
            # others.
            for education_form in education_forms:
                if education_form.is_valid() is False:
                    valid_flag = False
                    break

        # All forms are valid
        if valid_flag:
            print(education_forms[0].cleaned_data['institution'])
            pass

    else:
        personal_form = PersonalDetailsForm

        for i in range(0, collapse_id):
            education_forms.append(EducationForm)

    context = {
        "personal_form": personal_form,
        "education_forms": education_forms,
        "collapse_id": collapse_id,
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