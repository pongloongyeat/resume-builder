from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import PersonalDetails


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