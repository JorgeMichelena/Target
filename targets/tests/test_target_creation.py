from targets.factory import TopicFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from rest_framework import status
from random import randint, uniform
from django.urls import reverse


class CreateTargetTest(APITestCase):
    def setUp(self):
        self.topic = TopicFactory()
        self.user = UserFactory()
        self.title = faker.Faker().word()
        self.radius = randint(0, 1000)
        self.latitude = uniform(-180, 180)
        self.longitude = uniform(-90, 90)
        self.location = {"type": "Point",
                         "coordinates": [self.latitude, self.longitude]
                         }
        self.location_str = str(self.location)
        self.targets_url = reverse('target-list')

    def test_create_target_when_logged_in(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": self.title,
                "location": self.location_str,
                "radius": self.radius,
                "topic": self.topic.pk
                }
        expected = data.copy()
        expected['location'] = self.location
        response = self.client.post(self.targets_url, data)
        response_content = response.json()
        response_content.pop('pk')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_content, expected)

    def test_create_target_when_not_logged_in(self):
        data = {"title": self.title,
                "location": self.location_str,
                "radius": self.radius,
                "topic": self.topic.pk,
                }
        response = self.client.post(self.targets_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_target_when_logged_in_with_incorrect_values(self):
        self.client.force_authenticate(user=self.user)
        data_empty_title = {
            "title": '',
            "location": self.location_str,
            "radius": self.radius,
            "topic": self.topic.pk,
        }
        data_negative_radius = {
            "title": self.title,
            "location": self.location_str,
            "radius": -1*self.radius,
            "topic": self.topic.pk,
        }
        wlocation = str({"type": "Point",
                        "coordinates": [10000, 10000]
                         })
        data_wrong_location = {
            "title": self.title,
            "location": wlocation,
            "radius": self.radius,
            "topic": self.topic.pk,
        }
        data_nonexisting_topic = {
            "title": self.title,
            "location": self.location_str,
            "radius": self.radius,
            "topic": "wrong topic",
        }
        response_empty_title = self.client.post(self.targets_url, data_empty_title)
        response_negative_radius = self.client.post(self.targets_url, data_negative_radius)
        response_wrong_location = self.client.post(self.targets_url, data_wrong_location)
        response_nonexisting_topic = self.client.post(self.targets_url, data_nonexisting_topic)
        self.assertEqual(response_empty_title.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_negative_radius.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_wrong_location.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_nonexisting_topic.status_code, status.HTTP_400_BAD_REQUEST)
