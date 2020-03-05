import factory
from factory.faker import faker
from targets.models import Topic, Target
import random
from django.contrib.gis.geos import Point


class TopicFactory(factory.Factory):

    name = factory.Sequence(lambda n: f'Topic{n}')
    
    class Meta:
        model = Topic    

class TargetFactory(factory.Factory):
    title = faker.Faker().word()
    radius = random.randint(0, 1000)
    location = Point(random.randint(-90, 90) + random.random(),
                    random.randint(-180, 180) + random.random()
                )
    class Meta:
        model = Target
