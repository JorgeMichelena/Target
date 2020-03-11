
from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRF_ValidationError
from django.utils.translation import gettext_lazy as _

def validate_coordinates(value):
    latitude = value.x
    longitude = value.y
    if latitude>180 or latitude<-180:
        raise ValidationError(
            _('Latitude must be a real number between -180 and 180'), 
        )
    if longitude>90 or longitude<-90:
        raise ValidationError(
            _('Longitude must be a real number between -90 and 90'), 
        )

def less_than_10_targets(user):
    if len(user.targets.all())>=10:
        raise DRF_ValidationError(
            _('You must have less than 10 targets to be able to create a new one')
       )
    