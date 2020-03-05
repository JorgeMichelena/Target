from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    NOT_SPECIFIED = 'N'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_SPECIFIED, 'Not Specified'),
    ]
    
    gender = models.CharField(
        choices=GENDERS,
        max_length=1,
        default='',
    )
