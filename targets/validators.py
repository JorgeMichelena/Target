
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_coordinates(value):
    latitude = value.x
    longitude = value.y
    if latitude>90 or latitude<-90:
        raise ValidationError(
            _('Latitude must be a real number between -90 and 90'), 
        )
    if longitude>180 or longitude<-180:
        raise ValidationError(
            _('Longitude must be a real number between -180 and 180'), 
        )
