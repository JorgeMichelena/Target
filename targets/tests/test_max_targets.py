from targets.factory import TargetFactory
from factory.faker import faker
from users.factory import UserFactory
from rest_framework.test import APITestCase
from rest_framework import status
from random import randint, uniform
from django.urls import reverse
from django.conf import settings


class MaxTargetsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.targets = TargetFactory.create_batch(settings.MAX_TARGETS, user=self.user)
        self.to_delete_pk = self.targets[0].pk
        latitude = uniform(-180, 180)
        longitude = uniform(-90, 90)
        location = str({"type": "Point",
                        "coordinates": [latitude, longitude]
                        })
        self.data = {
            "title": faker.Faker().word(),
            "location": location,
            "radius": randint(0, 1000),
            "topic": self.targets[0].topic.pk
        }
        self.targets_url = reverse('target-list')

    def test_create_target_already_having_ten(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.targets_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         [f'You must have less than {settings.MAX_TARGETS} targets to be able to create a new one'])

    def test_create_after_deleting_one(self):
        to_delete_url = reverse('target-detail', kwargs={'pk': self.to_delete_pk})
        self.client.force_authenticate(self.user)
        self.client.delete(to_delete_url)
        response = self.client.post(self.targets_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
