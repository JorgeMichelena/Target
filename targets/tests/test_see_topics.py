from targets.factory import TopicFactory
from users.factory import UserFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class SeeTopicsTest(APITestCase):

    def setUp(self):
        topics = TopicFactory.create_batch(5)
        for topic in topics:
            topic.save()
        self.user = UserFactory()
        self.topics_url = reverse('topic-list')

    def test_see_topics_when_logged_in(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.topics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

    def test_see_topics_when_not_logged_in(self):
        response = self.client.get(self.topics_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
