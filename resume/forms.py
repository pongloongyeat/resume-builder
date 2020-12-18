from django import forms
from phonenumber_field.formfields import PhoneNumberField
from month.forms import MonthField
from .models import PersonalDetails, EducationDetails


class PersonalDetailsForm(forms.Form):
    first_name      = forms.CharField(max_length=30, required=True)
    last_name       = forms.CharField(max_length=30, required=True)
    email_address   = forms.EmailField(required=True)
    phone           = PhoneNumberField(required=False)
    about_me        = forms.CharField(widget=forms.Textarea(), max_length=300, required=False)

    # Stying-related
    first_name.widget.attrs.update({
        "class": "form-control"
    })
    last_name.widget.attrs.update({
        "class": "form-control"
    })
    email_address.widget.attrs.update({
        "class": "form-control"
    })
    phone.widget.attrs.update({
        "class": "form-control"
    })
    about_me.widget.attrs.update({
        "class": "form-control",
        "rows": 4
    })

    class Meta:
        model = PersonalDetails
        fields = ["first_name", "last_name", "email_address", "phone", "about_me"]

class EducationForm(forms.Form):
    institution = forms.CharField(max_length=50)
    course      = forms.CharField(max_length=75)
    start_date  = MonthField()
    end_date    = MonthField()
    country     = forms.CharField(max_length=60) # Longest belongs to UK with 56 chars!
    description = forms.CharField(widget=forms.Textarea(), max_length=300)

    # Stying-related
    institution.widget.attrs.update({
        "class": "form-control"
    })
    course.widget.attrs.update({
        "class": "form-control"
    })
    start_date.widget.attrs.update({
        "class": "form-control",
        "placeholder": "YYYY"
    })
    end_date.widget.attrs.update({
        "class": "form-control",
        "placeholder": "YYYY"
    })
    country.widget.attrs.update({
        "class": "form-control",
    })
    description.widget.attrs.update({
        "class": "form-control",
        "rows": 4
    })

    class Meta:
        model = EducationDetails
        fields = ["institution", "course", "start_date", "end_date", "country", "description"]