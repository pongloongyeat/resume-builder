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
    institution = forms.CharField(max_length=50, required=False)
    course      = forms.CharField(max_length=75, required=False)
    start_date  = MonthField(required=False)
    end_date    = MonthField(required=False)
    country     = forms.CharField(max_length=60, required=False) # Longest belongs to UK with 56 chars!
    description = forms.CharField(widget=forms.Textarea(), max_length=300, required=False)

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