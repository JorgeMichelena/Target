from rest_framework.test import APITestCase
from users.factory import UserFactory
from users.models import OnesignalPlayerId
from targets.factory import TopicFactory, TargetFactory
import factory
import random
from unittest.mock import patch
from django.urls import reverse


@patch('targets.views.send_notification')
class MatchTest(APITestCase):

    def setUp(self):
        target = TargetFactory()
        self.topic1 = target.topic
        self.user1 = target.user
        self.num_targets = random.randint(0, 9)
        TargetFactory.create_batch(self.num_targets,
                                   topic=self.topic1,
                                   user=self.user1,
                                   location=target.location
                                   )
        self.onesignal1 = OnesignalPlayerId(user=self.user1)
        self.onesignal1.save()
        self.user2 = UserFactory()
        self.user3 = UserFactory()
        lat = target.location.x
        lon = target.location.y
        location = str({'type': 'point',
                        'coordinates': [lat, lon]
                        })
        self.data = {
            'title': factory.Faker('word').generate(),
            'location': location,
            'radius': random.randint(0, 10000),
            'topic': self.topic1.pk
        }
        self.targets_url = reverse('target-list')

    def test_send_notification_for_every_match(self, send_notification_mock):
        self.client.force_authenticate(self.user2)
        self.client.post(self.targets_url, self.data)
        self.assertEqual(send_notification_mock.call_count, self.num_targets+1)

    def test_dont_send_notification_when_there_is_no_match(self, send_notification_mock):
        self.client.force_authenticate(self.user2)
        self.data['topic'] = TopicFactory()
        self.client.post(self.targets_url, self.data)
        send_notification_mock.assert_not_called()
