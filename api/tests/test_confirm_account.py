from factory.faker import faker
from rest_framework.test import APITestCase
from rest_framework import status
from django.core import mail
from django.urls import reverse
import re


class ConfirmEmailTest(APITestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.url_register = reverse('rest_register')
        self.url_login = reverse('rest_login')

    def test_signup_after_confirming_email(self):
        email = self.fake.email()
        password = self.fake.password()
        uname = self.fake.word()
        data = {'username': uname,
                'email': email,
                'password1': password,
                'password2': password,
                'gender': 'M',
                }
        response_signup = self.client.post(self.url_register, data)
        message = mail.outbox[0].body
        words_in_message = re.findall(r"[^\s]+", message)
        confirmation_url = words_in_message[-6]
        self.client.get(confirmation_url)
        response_login = self.client.post(self.url_login,
                                          {'username': uname,
                                           'email': email,
                                           'password': password}
                                          )
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

    def test_signup_without_confirming_email(self):
        email = self.fake.email()
        password = self.fake.password()
        uname = self.fake.word()
        data = {'username': uname,
                'email': email,
                'password1': password,
                'password2': password,
                'gender': 'M',
                }
        response_signup = self.client.post(self.url_register, data)
        response_login = self.client.post(self.url_login,
                                          {'username': uname,
                                           'email': email,
                                           'password': password
                                           }
                                          )
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_login.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_login.json()['non_field_errors'], ['E-mail is not verified.'])
