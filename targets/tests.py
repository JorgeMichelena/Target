from targets.factory import TopicFactory
from users.factory import UserFactory
from factory.faker import faker
from rest_framework.test import APITestCase
from api import serializers
from targets.models import Topic
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from targets.views import TopicsList
import json

class SeeTopicsTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        TopicFactory().save()
        self.user = UserFactory()
        self.view = TopicsList.as_view()
    
    def test_see_topics_when_logged_in(self):
        request = self.factory.get('api/v1/topics')
        force_authenticate(request, self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

