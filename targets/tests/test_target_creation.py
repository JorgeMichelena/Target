from targets.factory import TopicFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from targets.models import Topic
from rest_framework import status
from rest_framework.test import force_authenticate
from targets.views import TopicsList
import json
import random


class CreateTargetTest(APITestCase):
    def setUp(self):
        self.topic = TopicFactory()
        self.topic.save()
        self.user = UserFactory()
        self.user.save()
        self.title = faker.Faker().word()
        self.radius = random.randint(0, 1000) 
        latitude = random.randint(-90,90) + random.random()
        longitude = random.randint(-180,180) + random.random()
        self.location = str({"type": "Point",
                        "coordinates": [latitude, longitude]
                        })
    
    def test_create_target_when_logged_in(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": self.title,
            "location": self.location,
            "radius": self.radius,
            "topic": self.topic.name,
        }
        response = self.client.post('/api/v1/create-target/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_target_when_not_logged_in(self):
        data = {
            "title": self.title,
            "location": self.location,
            "radius": self.radius,
            "topic": self.topic.name,
        }
        response = self.client.post('/api/v1/create-target/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_target_when_logged_in_with_incorrect_values(self):
        self.client.force_authenticate(user=self.user)
        data_empty_title = {
            "title": '',
            "location": self.location,
            "radius": self.radius,
            "topic": self.topic.name,
        }
        data_negative_radius = {
            "title": self.title,
            "location": self.location,
            "radius": -1*self.radius,
            "topic": self.topic.name,
        }
        wlocation = str({"type": "Point",
                        "coordinates": [10000, 10000]
                        })
        data_wrong_location = {
            "title": self.title,
            "location": wlocation,
            "radius": self.radius,
            "topic": self.topic.name,
        }
        data_nonexisting_topic = {
            "title": self.title,
            "location": self.location,
            "radius": self.radius,
            "topic": "wrong topic",
        }
        response_empty_title = self.client.post('/api/v1/create-target/', data_empty_title)
        response_negative_radius = self.client.post('/api/v1/create-target/', data_negative_radius)
        response_wrong_location = self.client.post('/api/v1/create-target/', data_wrong_location)
        response_nonexisting_topic = self.client.post('/api/v1/create-target/', data_nonexisting_topic)
        self.assertEqual(response_empty_title.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_negative_radius.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_wrong_location.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_nonexisting_topic.status_code, status.HTTP_400_BAD_REQUEST)

