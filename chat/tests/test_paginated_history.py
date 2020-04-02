from rest_framework.test import APITestCase
from users.factory import UserFactory
from targets.models import Topic, Target
from chat.models import Match
from rest_framework import status
from rest_framework.test import force_authenticate
from targets.factory import TopicFactory, TargetFactory
from targets.factory import truncate
from chat.factory import MessageFactory
import factory
import random
import json
from django.test import Client, TestCase

class PaginatedHistoryTest(TestCase):
    def setUp(self):
        num_messages = 60
        
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user1.save()
        self.user2.save()
        self.topic = TopicFactory()
        self.topic.save()
        self.target1 = TargetFactory(user=self.user1, topic=self.topic)
        self.target2 = TargetFactory(user=self.user2, topic=self.topic)
        self.target1.save()
        self.target2.save()
        self.match = Match(target1=self.target1, target2=self.target2)
        self.match.save()

        self.messages = []
        for i in range(num_messages):
            if i%2==0:
                self.messages.append(MessageFactory(author=self.user1, chat=self.match))
            else:
                self.messages.append(MessageFactory(author=self.user2, chat=self.match))
        
        for msg in self.messages:
            msg.save()

        
    def test_see_paginated_history_newest_20_messages_by_default(self):
        self.client.force_login(self.user1)
        response = self.client.get(f'/chat/{self.match.id}/')
        expected_page1 = ''
        for i in range(20):
            expected_page1 += '>>' + self.messages[40+i].author.username + ':\n' + self.messages[40+i].content + '\n\n'
        self.assertEqual(response.context['chat'], expected_page1)

    def test_see_paginated_history_indicating_page(self):
        self.client.force_login(self.user1)
        response1 = self.client.get(f'/chat/{self.match.id}/1/')
        expected_page1 = ''
        for i in range(20):
            expected_page1 += '>>' + self.messages[40+i].author.username + ':\n' + self.messages[40+i].content + '\n\n'
        response2 = self.client.get(f'/chat/{self.match.id}/2/')
        expected_page2 = ''
        for i in range(20):
            expected_page2 += '>>' + self.messages[20+i].author.username + ':\n' + self.messages[20+i].content + '\n\n'
        response3 = self.client.get(f'/chat/{self.match.id}/3/')
        expected_page3 = ''
        for i in range(20):
            expected_page3 += '>>' + self.messages[i].author.username + ':\n' + self.messages[i].content + '\n\n'
        
        self.assertEqual(response1.context['chat'], expected_page1)
        self.assertEqual(response2.context['chat'], expected_page2)
        self.assertEqual(response3.context['chat'], expected_page3)
