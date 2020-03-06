from targets.models import Topic
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import viewsets, permissions

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = (permissions.IsAuthenticated,)

class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = (permissions.IsAuthenticated,)


