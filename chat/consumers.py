import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Match
from django.db.models import F


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.user = self.scope['user']
        self.match = Match.objects.get(pk=self.match_id).select_related('target1', 'target2')
        self.room_group_name = f'chat_{self.match_id}'
        
        self.num_user = 1
        if self.match.target2.user_id == self.user.id:
            self.num_user = 2
            self.match.user_2_online_count = F('user_2_online_count') + 1
        else:
            self.match.user_1_online_count = F('user_1_online_count') + 1
        self.match.save()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.match.mark_messages_as_seen(self.user.id)
        self.accept()

    def disconnect(self, close_code):
        if self.match.target2.user_id
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        if self.num_user == 2:
            self.match.user_2_online_count = F('user_2_online_count') - 1
        else:
            self.match.user_1_online_count = F('user_1_online_count') - 1
        self.match.save()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if self.match.chat_start is None:
            self.match.start_chat()
        new_message = Message(content=message, chat=self.match, author=self.user)
        new_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': self.user.username,
            }
        )

    def chat_message(self, event):
        message = event['message']
        author = event['author']

        self.send(text_data=json.dumps({
            'message': message,
            'author': author,
        }))
