import factory
from factory.faker import faker
from targets.models import Topic


class TopicFactory(factory.Factory):

    name = factory.Sequence(lambda n: f'Topic{n}')
    
    class Meta:
        model = Topic    
