from django.db import models
from django.utils import timezone


class Match(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    chat_start = models.DateTimeField(null=True)
    chat_end = models.DateTimeField(null=True)
    target1 = models.ForeignKey('targets.Target', on_delete=models.CASCADE, related_name='matches1')
    target2 = models.ForeignKey('targets.Target', on_delete=models.CASCADE, related_name='matches2')

    def startChat(self):
        self.chat_start = timezone.now()

    def endChat(self):
        self.chat_end = timezone.now()


class Message(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    date_seen = models.DateTimeField(null=True)
    chat = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='chatlog')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages')
