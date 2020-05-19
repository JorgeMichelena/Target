from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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
    profile_picture = models.ImageField(default=settings.DEFAULT_PROFILE_PICTURE,
                                        upload_to=settings.PROFILE_PICTURE_FOLDER)


class OnesignalPlayerId(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='player_ids')
    player_id = models.CharField(max_length=40, default='')
