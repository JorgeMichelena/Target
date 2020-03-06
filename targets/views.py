from targets.models import Topic
from api.serializers import TopicSerializer
from rest_framework import viewsets, permissions

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)
