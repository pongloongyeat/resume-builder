from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PersonalDetails(models.Model):
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    email_address   = models.EmailField()
    phone           = PhoneNumberField(null=True, blank=True)
    about_me        = models.CharField(max_length=300, null=True, blank=True)