from factory.faker import faker
from targets.models import Topic, Target
from users.factory import UserFactory
from django.contrib.gis.geos import Point
from factory.django import DjangoModelFactory as Factory
import random
import math
import factory


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class TopicFactory(Factory):
    name = factory.Sequence(lambda n: f'Topic{n}')

    class Meta:
        model = Topic


class TargetFactory(Factory):
    title = faker.Faker().word()
    radius = random.randint(0, 1000)
    lat = float(random.randint(-180, 180)) + truncate(random.random(), 5)
    lon = float(random.randint(-90, 90)) + truncate(random.random(), 5)
    location = Point(lat, lon)
    topic = factory.SubFactory(TopicFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Target
        exclude = ('lat', 'lon',)
