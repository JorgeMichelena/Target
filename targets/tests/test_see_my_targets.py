from targets.factory import TopicFactory, TargetFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Topic
from rest_framework import status
from rest_framework.test import force_authenticate
from targets.views import TopicsList
import json
import random

class SeeMyTargetsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.user2 = UserFactory()
        self.user2.save()
        topic = TopicFactory()
        topic.save()
        self.target_1 = TargetFactory(user=self.user, topic=topic)
        self.target_2 = TargetFactory(user=self.user, topic=topic)
        self.target_3 = TargetFactory(user=self.user, topic=topic)
        self.target_1.save()
        self.target_2.save()
        self.target_3.save()

    def test_see_my_targets_when_logged_in(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/v1/my-targets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['title'], self.target_1.title)
        self.assertEqual(response.json()[1]['title'], self.target_2.title)
        self.assertEqual(response.json()[2]['title'], self.target_3.title)

    def test_see_my_targets_when_not_logged_in(self):
        response = self.client.get('/api/v1/my-targets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_different_user_cant_see_my_targets(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get('/api/v1/my-targets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)