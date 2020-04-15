from targets.factory import TargetFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class DeleteTargetTest(APITestCase):
    def setUp(self):
        self.target_1 = TargetFactory()
        topic = self.target_1.topic
        self.user = self.target_1.user
        self.target_2 = TargetFactory(user=self.user, topic=topic)
        self.target_3 = TargetFactory(topic=topic)
        self.user2 = self.target_3.user
        self.targets_url = reverse('target-list')

    def test_delete_my_target(self):
        self.client.force_authenticate(self.user)
        target1_url = reverse('target-detail', args=[self.target_1.pk])
        response_delete = self.client.delete(target1_url)
        response_get = self.client.get(self.targets_url)
        expected_target = {'pk': self.target_2.pk,
                           'title': self.target_2.title,
                           'location': {'type': 'Point',
                                        'coordinates': [self.target_2.location.x,
                                                        self.target_2.location.y]},
                           'radius': self.target_2.radius,
                           'topic': self.target_2.topic.pk,
                           }
        expected_list = [expected_target]
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response_get.json()), 1)
        self.assertCountEqual(response_get.json(), expected_list)

    def test_delete_when_not_logged_in(self):
        target1_url = reverse('target-detail', args=[self.target_1.pk])
        response = self.client.delete(target1_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_delete_other_users_targets(self):
        self.client.force_authenticate(self.user)
        target3_url = reverse('target-detail', args=[self.target_3.pk])
        response_delete = self.client.delete(target3_url)
        self.client.logout()
        self.client.force_authenticate(self.user2)
        response_get = self.client.get(self.targets_url)
        expected_target = {'pk': self.target_3.pk,
                           'title': self.target_3.title,
                           'location': {'type': 'Point',
                                        'coordinates': [self.target_3.location.x,
                                                        self.target_3.location.y]},
                           'radius': self.target_3.radius,
                           'topic': self.target_3.topic.pk,
                           }
        expected_list = [expected_target]
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response_get.json()), 1)
        self.assertEqual(response_get.json(), expected_list)
