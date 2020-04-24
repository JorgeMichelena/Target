from django.db import models
from django.utils import timezone


class Match(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    chat_start = models.DateTimeField(null=True)
    target1 = models.ForeignKey('targets.Target', on_delete=models.CASCADE, related_name='matches1')
    target2 = models.ForeignKey('targets.Target', on_delete=models.CASCADE, related_name='matches2')

    def start_chat(self):
        self.chat_start = timezone.now()

    def mark_messages_as_seen(self, user_id):
        (self.chatlog
            .filter(date_seen__isnull=True)
            .order_by('id')
            .exclude(author__id=user_id)
         ).update(date_seen=timezone.now())


class Message(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    date_seen = models.DateTimeField(null=True)
    chat = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='chatlog')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages')

    def seen(self):
        self.date_seen = timezone.now()
