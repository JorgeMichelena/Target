import factory
from factory.faker import faker
from targets.models import Topic


class TopicFactory(factory.Factory):
    
    name = faker.Faker().word()
    
    class Meta:
        model = Topic    
