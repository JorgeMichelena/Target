from rest_framework.test import APITestCase
from users.factory import UserFactory
from targets.models import Topic, Target
from chat.models import Match
from rest_framework import status
from rest_framework.test import force_authenticate
from targets.factory import TopicFactory
from targets.factory import truncate
import factory
import random
import json


class MatchTest(APITestCase):

    def setUp(self):
        self.topic1 = TopicFactory()
        self.topic2 = TopicFactory()
        self.topic1.save()
        self.topic2.save()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user1.save()
        self.user2.save()
        lat = truncate(random.uniform(-180, 150), 5)
        lon = truncate(random.uniform(-90, 70), 5)
        location1 = str({'type': 'point',
                     'coordinates':[lat,lon]
                    })
        location2 = str({'type': 'point',
                     'coordinates':[lat+1,lon+1]
                    })
        location3 = str({'type': 'point',
                     'coordinates':[lat+20,lon+15]
                    })
        self.data1 = {
            'title' : factory.Faker('word').generate(),
            'location' : location1,
            'radius': random.randint(70000, 1000000),
            'topic': self.topic1.name
        }
        self.data2 = {
            'title' : factory.Faker('word').generate(),
            'location' : location2,
            'radius': random.randint(70000, 1000000),
            'topic': self.topic1.name
        }
        self.data3 = {
            'title' : factory.Faker('word').generate(),
            'location' : location2,
            'radius': random.randint(70000, 1000000),
            'topic': self.topic2.name
        }
        self.data4 = {
            'title' : factory.Faker('word').generate(),
            'location' : location3,
            'radius': random.randint(0, 7000),
            'topic': self.topic1.name
        }

    def test_create_targets_that_match(self):
        self.client.force_authenticate(user=self.user1)
        self.client.post('/api/v1/targets/', self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        self.client.post('/api/v1/targets/', self.data2)
        u1_target = self.user1.targets.all()[0]
        u2_target = self.user2.targets.all()[0]
        match = Match.objects.all()[0]
        self.assertEqual(match.target1, u2_target)
        self.assertEqual(match.target2, u1_target)

    def test_create_targets_in_range_with_different_topic(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post('/api/v1/targets/', self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        response2 = self.client.post('/api/v1/targets/', self.data3)
        matches = Match.objects.all()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(matches), 0)

    def test_create_targets_not_in_range_with_same_topic(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post('/api/v1/targets/', self.data1)
        self.client.logout
        self.client.force_authenticate(user=self.user2)
        response2 = self.client.post('/api/v1/targets/', self.data4)
        matches = Match.objects.all()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(matches), 0)

    def test_create_targets_that_would_match_but_are_made_by_same_user(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post('/api/v1/targets/', self.data1)
        response2 = self.client.post('/api/v1/targets/', self.data2)
        matches = Match.objects.all()
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(matches), 0)  
