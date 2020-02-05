from django.db import models

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
    interest = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    grade = models.CharField(max_length=2, default="#")
    shortlisted = models.BooleanField(default=False)
