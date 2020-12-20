from django.contrib import admin
from resume.models import Resume, PersonalDetails, EducationDetails

# Register your models here.

admin.site.register(Resume)
admin.site.register(PersonalDetails)
admin.site.register(EducationDetails)