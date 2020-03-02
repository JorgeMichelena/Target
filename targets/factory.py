import factory
from factory.faker import faker
from targets.models import Topic


class TopicFactory(factory.Factory):
    
    name = factory.Sequence(lambda n: 'Topic%s' %n)
    
    class Meta:
        model = Topic    
