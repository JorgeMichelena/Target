from targets.models import Topic
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import generics, permissions, viewsets

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CreateTarget(generics.CreateAPIView):
    serializer_class = TargetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


