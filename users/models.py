from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        NOT_SPECIFIED = 'N', _('Not specified')

    gender = models.CharField(
        choices=Gender.choices,
        max_length=1,
        default='N',
    )
    onesignal_playerId = models.CharField(max_length=40, default='')
