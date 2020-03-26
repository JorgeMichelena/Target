from targets.models import Topic
from chat.models import Match
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import viewsets, permissions
from targets.validators import less_than_10_targets
from django.contrib.gis.db.models.functions import Distance


class TopicViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TargetViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TargetSerializer

    def perform_create(self, serializer):
        target = serializer.save(user=self.request.user)
        for compatible in target.compatible_targets():
            match = Match(target1=target, target2=compatible)
            match.save()

    def get_queryset(self):
        return self.request.user.targets

def search_for_match(target_title):
    target = Target.objects.get(title=target_title)
    for candidate in Target.objects.annotate(distance=Distance('location', target.location)):
        if candidate.distance.m <= candidate.radius+target.radius and candidate.topic == target.topic and candidate.user!=target.user:
            match = Match(target1=target, target2=candidate)
            match.save()
