from django.db import models
from django.contrib.gis.db import models as gis_models
from targets.validators import validate_coordinates


class Topic(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
<<<<<<< HEAD
    picture = models.TextField(default='')
=======
    picture = models.ImageField(upload_to='media/topic_pictures/', null=True)
    def __str__(self):
        return self.name

class Target(gis_models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targets')
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    radius = models.PositiveIntegerField()
    location = gis_models.PointField(geography=True, validators=[validate_coordinates])
>>>>>>> 20b9712... Add create target functionality
