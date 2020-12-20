from django import forms
from .models import PersonalDetails


class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ['first_name', 'last_name', 'email_address', 'phone', 'about_me']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 4}),
        }