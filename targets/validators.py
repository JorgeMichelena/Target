from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRF_ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def validate_coordinates(value):
    latitude = value.x
    longitude = value.y
    if latitude > 180 or latitude < -180:
        raise ValidationError(
            _('Latitude must be a real number between -180 and 180'),
        )
    if longitude > 90 or longitude < -90:
        raise ValidationError(
            _('Longitude must be a real number between -90 and 90'),
        )


def less_than_max_targets(user):
    if user.targets.count() >= settings.MAX_TARGETS:
        raise DRF_ValidationError(
            _(f'You must have less than {settings.MAX_TARGETS} targets to be able to create a new one')
        )
