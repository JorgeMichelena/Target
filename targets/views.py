from targets.models import Topic
from chat.models import Match
from api.serializers import TopicSerializer, TargetSerializer
from rest_framework import viewsets, permissions
from chat.push_notifications import send_notification


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
            player_ids = compatible.user.player_ids.all()
            if player_ids:
                ids_list = [pid.player_id for pid in player_ids]
                message = f'New match with {self.request.user.username}'
                send_notification('Match', match.id, message, ids_list)

    def get_queryset(self):
        return self.request.user.targets
