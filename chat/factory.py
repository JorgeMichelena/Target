from factory.django import DjangoModelFactory as Factory
from chat.models import Match
from factory import SubFactory
from targets.factory import TargetFactory


class MatchFactory(Factory):
    target1 = SubFactory(TargetFactory)
    target2 = SubFactory(TargetFactory)

    class Meta:
        model = Match
