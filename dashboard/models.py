from django.db import models

# Create your models here.


class InterestForm(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)

    def __str__(self):
        return self.name
