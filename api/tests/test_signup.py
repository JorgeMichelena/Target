from factory.faker import faker
from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse


class SignupTest(APITestCase):

    def setUp(self):
        self.fake = faker.Faker()
        self. register_url = reverse('rest_register')

    def test_signup_with_correct_values(self):
        uname = self.fake.word()
        email = self.fake.email()
        pass_1 = self.fake.password()
        data = {'username': uname,
                'email': email,
                'password1': pass_1,
                'password2': pass_1,
                'gender': User.Gender.MALE,
                }
        response = self.client.post(self.register_url, data)
        user = User.objects.get(username=uname)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, uname)
        self.assertEqual(user.gender, User.Gender.MALE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_incorrect_gender_value(self):
        uname = self.fake.word()
        email = self.fake.email()
        pass_1 = self.fake.password()
        data = {'username': uname,
                'email': email,
                'password1': pass_1,
                'password2': pass_1,
                'gender': 'H',
                }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['gender'], ["\"H\" is not a valid choice."])

    def test_signup_with_username_already_in_use(self):
        uname = self.fake.word()
        email_1 = self.fake.email()
        email_2 = self.fake.email()
        pass_1 = self.fake.password()
        pass_2 = self.fake.password()
        data_1 = {'username': uname,
                  'email': email_1,
                  'password1': pass_1,
                  'password2': pass_1,
                  'gender': User.Gender.MALE,
                  }
        data_2 = {'username': uname,
                  'email': email_2,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': User.Gender.FEMALE,
                  }
        self.client.post(self.register_url, data_1)
        response_2 = self.client.post(self.register_url, data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.json()['username'], ['A user with that username already exists.'])

    def test_signup_with_email_already_in_use(self):
        uname = self.fake.word()
        email = self.fake.email()
        pass_1 = self.fake.password()
        pass_2 = self.fake.password()
        data_1 = {'username': uname,
                  'email': email,
                  'password1': pass_1,
                  'password2': pass_1,
                  'gender': User.Gender.FEMALE,
                  }
        data_2 = {'username': 'TestUser2',
                  'email': email,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': User.Gender.MALE,
                  }
        self.client.post(self.register_url, data_1)
        response_2 = self.client.post(self.register_url, data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.json()['email'], ['A user is already registered with this e-mail address.'])
