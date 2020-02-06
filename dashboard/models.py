from django.db import models
from django.utils import timezone

# Create your models here.


class InterestForm(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=50, default='#' * 15)
    pincode = models.CharField(max_length=10, default='######')

    def __str__(self):
        return self.name


class ExperienceForm(models.Model):
    description = models.TextField(default="No Description")
    interest = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default='example@example.com')
    experience = models.CharField(max_length=100)
    grade = models.CharField(max_length=2, default="N/A")
    shortlisted = models.BooleanField(default=False)


class PhoneInterview(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    timing = models.CharField(max_length=100,default="Not Confirmed")
    grade = models.CharField(max_length=2, default="N/A")
    accepted = models.BooleanField(default=False)
