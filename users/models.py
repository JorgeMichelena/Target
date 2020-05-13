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


class OnesignalPlayerId(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='player_ids')
    player_id = models.CharField(max_length=40, default='')
