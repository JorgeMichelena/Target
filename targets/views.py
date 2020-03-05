from targets.models import Topic
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import generics, permissions

class TopicsList(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = (permissions.IsAuthenticated,)

class CreateTarget(generics.CreateAPIView):
    serializer_class = TargetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SeeMyTargets(generics.ListAPIView):
    serializer_class = TargetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        return user.targets.all()


