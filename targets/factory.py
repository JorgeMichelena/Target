from targets.models import Topic, Target
from users.factory import UserFactory
from django.contrib.gis.geos import Point
from factory.django import DjangoModelFactory as Factory
from faker.providers import BaseProvider
import random
import factory


class DjangoGeoPointProvider(BaseProvider):

    def geo_point(self, **kwargs):
        kwargs['coords_only'] = True
        faker = factory.Faker('local_latlng', **kwargs)
        coords = faker.generate()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class TopicFactory(Factory):
    name = factory.Faker('word')

    class Meta:
        model = Topic


class TargetFactory(Factory):
    factory.Faker.add_provider(DjangoGeoPointProvider)

    title = factory.Faker('word')
    radius = random.randint(0, 1000)
    location = factory.Faker('geo_point')
    topic = factory.SubFactory(TopicFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Target
