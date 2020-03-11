from targets.factory import TopicFactory, TargetFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Topic, Target
from rest_framework import status
from rest_framework.test import force_authenticate
import random
from targets.factory import truncate

import json

class MaxTargetsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        topic = TopicFactory()
        topic.save()
        self.targets = TargetFactory.create_batch(10, user=self.user, topic=topic)
        for target in self.targets:
            target.save()
        self.target_pk = Target.objects.all()[0].pk
        latitude = random.randint(-180,180) + truncate(random.random(), 5)
        longitude = random.randint(-90,90) + truncate(random.random(), 5)
        location = str({"type": "Point",
                    "coordinates": [latitude, longitude]
                    })
        self.data = {
            "title": faker.Faker().word(),
            "location": location,
            "radius": random.randint(0, 1000),
            "topic": topic.name
        }

    def test_create_target_already_having_ten(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/v1/targets/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['You must have less than 10 targets to be able to create a new one'])
    
    def test_create_after_deleting_one(self):
        self.client.force_authenticate(self.user)
        self.client.delete(f'/api/v1/targets/{self.target_pk}/')
        response = self.client.post('/api/v1/targets/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
