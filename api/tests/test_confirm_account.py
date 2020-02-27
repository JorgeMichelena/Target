from factory.faker import faker
from rest_framework.test import APITestCase
from api import serializers
from users.models import User
from rest_framework import status
from rest_framework.test import APIClient
import json
from django.core import mail
import re

class ConfirmEmailTest(APITestCase):
    def setUp(self):
        self.fake = faker.Faker()

    def test_signup_after_confirming_email(self):
        email = self.fake.email()
        password = self.fake.password()
        data = {'username': 'TestUser',
                  'email': email,
                  'password1': password,
                  'password2': password,
                  'gender': 'M',
        }
        response_signup = self.client.post('/api/v1/registration/', data)
        message = mail.outbox[0].body
        words_in_message = re.findall(r"[^\s]+", message)
        confirmation_url = words_in_message[-6]
        self.client.get(confirmation_url)
        response_login = self.client.post('/api/v1/login/', {'username': 'TestUser','email':email , 'password': password})
        
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
    
    def test_signup_without_confirming_email(self):
        email = self.fake.email()
        password = self.fake.password()
        data = {'username': 'TestUser',
                  'email': email,
                  'password1': password,
                  'password2': password,
                  'gender': 'M',
        }
        response_signup = self.client.post('/api/v1/registration/', data)
        response_login = self.client.post('/api/v1/login/', {'username': 'TestUser','email':email , 'password': password})
        
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_login.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_login.json()['non_field_errors'], ['E-mail is not verified.'])
