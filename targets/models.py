from django.db import models
from django.contrib.gis.db import models as gis_models
from targets.validators import validate_coordinates


class Topic(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    picture = models.TextField(default='')
    def __str__(self):
        return self.name

class Target(gis_models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targets')
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    radius = models.PositiveIntegerField()
    location = gis_models.PointField(geography=True, validators=[validate_coordinates])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
