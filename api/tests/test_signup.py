from factory.faker import faker
from rest_framework.test import APITestCase
from api import serializers
from users.models import User
from rest_framework import status
from rest_framework.test import APIClient
import json
  
    
class SignupTest(APITestCase):
    def setUp(self):
        self.fake = faker.Faker()
        
    def test_signup_with_correct_values(self):
        email = self.fake.email()
        pass_1 = self.fake.password()
        data = {'username': 'TestUser',
                'email': email,
                'password1': pass_1,
                'password2': pass_1,
                'gender': User.MALE[0],
        }
        response = self.client.post('/api/v1/registration/', data)
        user = User.objects.get(username='TestUser')
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, 'TestUser')
        self.assertEqual(user.gender, User.MALE[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_signup_with_incorrect_gender_value(self):
        email = self.fake.email()
        pass_1 = self.fake.password()
        data = {'username': 'TestUser',
                'email': email,
                'password1': pass_1,
                'password2': pass_1,
                'gender': 'H',
        }
        response = self.client.post('/api/v1/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['gender'], ["\"H\" is not a valid choice."])
    
    def test_signup_with_username_already_in_use(self):
        email_1 = self.fake.email()
        email_2 = self.fake.email()
        pass_1 = self.fake.password()
        pass_2 = self.fake.password()        
        data_1 = {'username': 'TestUser',
                  'email': email_1,
                  'password1': pass_1,
                  'password2': pass_1,
                  'gender': User.MALE[0],
        }
        data_2 = {'username': 'TestUser',
                  'email': email_2,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': User.FEMALE[0],
        }
        self.client.post('/api/v1/registration/', data_1)
        response_2 = self.client.post('/api/v1/registration/', data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.json()['username'], ['A user with that username already exists.'])     
    
    def test_signup_with_email_already_in_use(self):
        email = self.fake.email()
        pass_1 = self.fake.password()
        pass_2 = self.fake.password()
        data_1 = {'username': 'TestUser',
                  'email': email,
                  'password1': pass_1,
                  'password2': pass_1,
                  'gender': User.FEMALE[0],
        }
        data_2 = {'username': 'TestUser2',
                  'email': email,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': User.MALE[0],
        }
        self.client.post('/api/v1/registration/', data_1)
        response_2 = self.client.post('/api/v1/registration/', data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.json()['email'], ['A user is already registered with this e-mail address.'])
