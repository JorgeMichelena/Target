from django.db import models
from django.contrib.gis.db import models as gis_models
from targets.validators import validate_coordinates
from django.conf import settings


class Topic(models.Model):
    name = models.CharField(max_length=30, unique=True)
    picture = models.ImageField(default=settings.DEFAULT_TOPIC_PICTURE,
                                upload_to=settings.TOPIC_PICTURE_FOLDER,
                                )

    def __str__(self):
        return self.name


class Target(gis_models.Model):
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             related_name='targets')
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, unique=True)
    radius = models.PositiveIntegerField()
    location = gis_models.PointField(geography=True,
                                     validators=[validate_coordinates])
    creation_date = models.DateField(auto_now_add=True)

    def compatible_targets(self):
        user = self.user
        radius = self.radius
        location = self.location
        topic = self.topic
        return Target.objects.filter(
                                location__distance_lte=(location,
                                                        models.F('radius') + radius),
                                topic_id=topic.pk
        ).exclude(user_id=user.id)
