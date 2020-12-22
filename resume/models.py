from django.db import models
from account.models import User
from phonenumber_field.modelfields import PhoneNumberField
from month.models import MonthField

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PersonalDetails(models.Model):
    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name      = models.CharField(max_length=30, blank=True)
    last_name       = models.CharField(max_length=30, blank=True)
    email_address   = models.EmailField(blank=True)
    phone           = PhoneNumberField(blank=True)
    about_me        = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class EducationDetails(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    institution = models.CharField(max_length=50, blank=True)
    course      = models.CharField(max_length=75, blank=True)
    start_date  = MonthField(blank=True)
    end_date    = MonthField(blank=True)
    country     = models.CharField(max_length=60, blank=True) # Longest belongs to UK with 56 chars!
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.institution

class WorkDetails(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    position        = models.CharField(max_length=50, blank=True)
    company_name    = models.CharField(max_length=75, blank=True)
    start_date      = MonthField(blank=True)
    end_date        = MonthField(blank=True)
    country         = models.CharField(max_length=60, blank=True) # Longest belongs to UK with 56 chars!
    description     = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return ("%s, %s" % (self.position, self.company_name))