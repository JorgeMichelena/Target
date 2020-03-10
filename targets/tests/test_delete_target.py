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

class DeleteTargetTest(APITestCase):
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
        self.target_3 = TargetFactory(user=self.user2, topic=topic)
        self.target_3.save()
        self.trg1_pk = self.user.targets.all()[0].pk
        self.trg3_pk = self.user2.targets.all()[0].pk

    def test_delete_my_target(self):
        self.client.force_authenticate(self.user)
        response_delete = self.client.delete(f'/api/v1/targets/{self.trg1_pk}/')
        response_get = self.client.get('/api/v1/targets/')
        expected_target = {'title': self.target_2.title,
                             'location': {'type':'Point',
                                          'coordinates': [self.target_2.location.x, self.target_2.location.y]},
                             'radius': self.target_2.radius,
                             'topic': self.target_2.topic.name,
                            }
        expected_list = [expected_target]
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response_get.json()), 1)
        self.assertCountEqual(response_get.json(), expected_list)

    def test_delete_when_not_logged_in(self):
        response = self.client.delete(f'/api/v1/targets/{self.trg1_pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_delete_other_users_targets(self):
        self.client.force_authenticate(self.user)
        response_delete = self.client.delete(f'/api/v1/targets/{self.trg3_pk}/')
        self.client.logout()
        self.client.force_authenticate(self.user2)
        response_get = self.client.get('/api/v1/targets/')
        expected_target = {'title': self.target_3.title,
                             'location': {'type':'Point',
                                          'coordinates': [self.target_3.location.x, self.target_3.location.y]},
                             'radius': self.target_3.radius,
                             'topic': self.target_3.topic.name,
                            }
        expected_list = [expected_target]
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response_get.json()), 1)
        self.assertEqual(response_get.json(), expected_list)
