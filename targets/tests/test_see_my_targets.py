from targets.factory import TopicFactory, TargetFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Topic, Target
from rest_framework import status
from rest_framework.test import force_authenticate
from api.serializers import TargetSerializer
from rest_framework.renderers import JSONRenderer
import json

class SeeMyTargetsTest(APITestCase):
    maxDiff = None
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        self.user2 = UserFactory()
        self.user2.save()
        topic = TopicFactory()
        topic.save()
        self.target_1 = TargetFactory(user=self.user, topic=topic)
        self.target_2 = TargetFactory(user=self.user, topic=topic)
        self.target_1.save()
        self.target_2.save()

    def test_see_my_targets_when_logged_in(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/v1/targets/')
        expected_target_1 = {'title': self.target_1.title,
                             'location': {'type':'Point',
                                          'coordinates': [self.target_1.location.x, self.target_1.location.y]},
                             'radius': self.target_1.radius,
                             'topic': self.target_1.topic.name,
                            }
        expected_target_2 = {'title': self.target_2.title,
                             'location': {'type':'Point',
                                          'coordinates': [self.target_2.location.x, self.target_2.location.y]},
                             'radius': self.target_2.radius,
                             'topic': self.target_2.topic.name,
                            }
        expected_list = [expected_target_1, expected_target_2]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertCountEqual(response.json(), expected_list)

    def test_see_my_targets_when_not_logged_in(self):
        response = self.client.get('/api/v1/targets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_different_user_cant_see_my_targets(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get('/api/v1/targets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)