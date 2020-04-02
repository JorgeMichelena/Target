from rest_framework import viewsets, permissions
from api.serializers import MatchSerializer
from chat.models import Match
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from users.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


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
        page = 1
        per_page = 20
        if 'page' in kwargs and kwargs['page']>0:
            page = kwargs['page']
        offset = (page-1)*per_page
        messages = match.chatlog.all().order_by('-date_sent').select_related('author')[offset : offset+per_page]
        chat = ''
        size = len(messages)
        for i in range(size):
            chat += '>>' + messages[size-i-1].author.username + ':\n' + messages[size-i-1].content + '\n\n'
        context['chat'] = chat
        context['num_page'] = page
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        match = get_object_or_404(Match, id=kwargs['match_id'])
        if not (match.target1.user == user or match.target2.user == user):
            raise Http404
        return super(ChatRoom, self).dispatch(request, *args, **kwargs)
