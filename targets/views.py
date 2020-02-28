from targets.models import Topic
from api.serializers import TopicSerializer
from rest_framework import generics, permissions

class TopicsList(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = (permissions.IsAuthenticated,)

