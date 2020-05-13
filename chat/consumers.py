import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Match


class ChatConsumer(WebsocketConsumer):
    connected = {}

    def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.user = self.scope['user']
        self.match = Match.objects.select_related('target1', 'target2').get(pk=self.match_id)
        if not (self.match.target1.user == self.user or self.match.target2.user == self.user):
            self.close()
        self.room_group_name = f'chat_{self.match_id}'
        self.partner_id = self.match.target1.user_id
        if self.user.id == self.partner_id:
            self.partner_id = self.match.target2.user_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.match.mark_messages_as_seen(self.user.id)
        connections = self.connected.setdefault(self.user.id, 0)
        self.connected[self.user.id] = connections + 1
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.connected[self.user.id] = self.connected[self.user.id] - 1

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if self.match.chat_start is None:
            self.match.start_chat()
        new_message = Message(content=message, chat=self.match, author=self.user)
        if self.partner_id in self.connected and self.connected[self.partner_id] > 0:
            new_message.seen()
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
