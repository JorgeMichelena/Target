from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    picture = models.TextField(default='')