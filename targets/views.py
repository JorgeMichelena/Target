from targets.models import Topic, Target
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import viewsets, permissions

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = (permissions.IsAuthenticated,)

class TargetViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TargetSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return self.request.user.targets
