from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MALE = ('M', 'Male')
    FEMALE = ('F', 'Female')
    OTHER = ('O', 'Other')
    NOT_SPECIFIED = ('N', 'Not Specified')
    GENDERS = (
        MALE,
        FEMALE,
        OTHER,
        NOT_SPECIFIED,
    )
    
    gender = models.CharField(
        choices=GENDERS,
        max_length=1,
        default='',
    )
