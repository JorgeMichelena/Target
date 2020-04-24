from rest_framework import viewsets, permissions
from api.serializers import MatchSerializer
from chat.models import Match
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MatchSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return (Match.objects
                     .filter(Q(target1__user_id=user_id) | Q(target2__user_id=user_id))
                     .select_related('target1', 'target2')
                )


class ChatRoom(TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, id=kwargs['match_id'])
        messages = match.chatlog.all().order_by('-creation_date').select_related('author')
        paginator = Paginator(messages, 20)
        page = 1
        if 'page' in self.request.GET and self.request.GET['page'].isdigit():
            if int(self.request.GET['page']) > paginator.num_pages:
                page = paginator.num_pages
            else:
                page = self.request.GET['page']
        chat = ''
        chatlog = paginator.page(page).object_list
        for msg in chatlog:
            chat = '>>' + msg.author.username + ':\n' + msg.content + '\n\n' + chat
        context['chat'] = chat
        context['num_page'] = page
        match.mark_messages_as_seen(self.request.user.id)
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        match = get_object_or_404(Match, id=kwargs['match_id'])
        if not (match.target1.user == user or match.target2.user == user):
            raise Http404
        return super(ChatRoom, self).dispatch(request, *args, **kwargs)
