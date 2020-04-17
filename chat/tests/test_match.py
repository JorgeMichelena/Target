from rest_framework.test import APITestCase
from users.factory import UserFactory
from chat.models import Match
from rest_framework import status
from targets.factory import TopicFactory
from random import randint, uniform
from django.urls import reverse
import factory


class MatchTest(APITestCase):

    def setUp(self):
        self.topic1 = TopicFactory()
        self.topic2 = TopicFactory()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        lat = uniform(-180, 150)
        lon = uniform(-90, 70)
        location1 = str({'type': 'point',
                         'coordinates': [lat, lon]
                         })
        location2 = str({'type': 'point',
                         'coordinates': [lat+1, lon+1]
                         })
        location3 = str({'type': 'point',
                         'coordinates': [lat+20, lon+15]
                         })
        self.data1 = {'title': factory.Faker('word').generate(),
                      'location': location1,
                      'radius': randint(70000, 1000000),
                      'topic': self.topic1.pk
                      }
        self.data2 = {'title': factory.Faker('word').generate(),
                      'location': location2,
                      'radius': randint(70000, 1000000),
                      'topic': self.topic1.pk
                      }
        self.data3 = {'title': factory.Faker('word').generate(),
                      'location': location2,
                      'radius': randint(70000, 1000000),
                      'topic': self.topic2.pk
                      }
        self.data4 = {'title': factory.Faker('word').generate(),
                      'location': location3,
                      'radius': randint(0, 7000),
                      'topic': self.topic1.pk
                      }
        self.targets_url = reverse('target-list')

    def test_create_targets_that_match(self):
        self.client.force_authenticate(user=self.user1)
        self.client.post(self.targets_url, self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        self.client.post(self.targets_url, self.data2)
        u1_target = self.user1.targets.all()[0]
        u2_target = self.user2.targets.all()[0]
        match = Match.objects.all()[0]
        self.assertEqual(match.target1, u2_target)
        self.assertEqual(match.target2, u1_target)

    def test_create_targets_in_range_with_different_topic(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post(self.targets_url, self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        response2 = self.client.post(self.targets_url, self.data3)
        matches = Match.objects.count()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(matches, 0)

    def test_create_targets_not_in_range_with_same_topic(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post(self.targets_url, self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        response2 = self.client.post(self.targets_url, self.data4)
        matches = Match.objects.count()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(matches, 0)

    def test_create_targets_that_would_match_but_are_made_by_same_user(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post(self.targets_url, self.data1)
        response2 = self.client.post(self.targets_url, self.data2)
        matches = Match.objects.count()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(matches, 0)
