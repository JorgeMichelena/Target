from factory.django import DjangoModelFactory as Factory
from chat.models import Match, Message
from factory import SubFactory
from targets.factory import TargetFactory
import factory


class MatchFactory(Factory):
    target1 = SubFactory(TargetFactory)
    target2 = SubFactory(TargetFactory)

    class Meta:
        model = Match


class MessageFactory(factory.Factory):
    class Meta:
        model = Message
    content = factory.Faker('text')
