from users.factory import UserFactory
from factory.faker import faker
from rest_framework.test import APITestCase
from api import serializers
from users.models import User
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory
from rest_auth.views import UserDetailsView
from rest_auth.registration.views import RegisterView
import json

class EditProfileTests(APITestCase):
        
    def setUp(self):
        self.request_factory = APIRequestFactory()
        self.user1 = UserFactory()
        self.view = UserDetailsView.as_view()
    
    def test_logged_user_changes_editable_fields(self):
        # arrange
        old_first_name = self.user1.first_name
        old_last_name = self.user1.last_name
        old_gender = self.user1.gender        
        data = {'username':self.user1.username, 
                'first_name':'new_first_name', 
                'last_name':'new_last_name', 
                'gender':'F',
        }
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name
        new_gender = self.user1.gender
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_first_name, 'new_first_name')
        self.assertEqual(new_last_name, 'new_last_name')
        self.assertEqual(new_gender, 'F')
        self.assertFalse(new_first_name==old_first_name)
        self.assertFalse(new_last_name==old_last_name)
        self.assertFalse(new_gender==old_gender)
        
    
    def test_logged_user_changes_pk(self):
        # arrange
        old_pk = self.user1.pk
        data = {'pk':'1000', 
                'username':self.user1.username,
        }
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_pk = self.user1.pk
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_pk, old_pk)
        self.assertFalse(new_pk=='1000')
        
    def test_logged_user_changes_email(self):
        # arrange
        old_email = self.user1.email
        data = {'username':self.user1.username, 
                'email':'newemail@example.com',
        }
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_email = self.user1.email
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_email, old_email)
        self.assertFalse(new_email=='newemail@example.com')
    
    def test_not_logged_user_changes_editable_fields(self):
        # arrange
        old_first_name = self.user1.first_name
        old_last_name = self.user1.last_name
        data = {'username':self.user1.username, 
                'first_name':'new_first_name', 
                'last_name':'new_last_name',
        }
        request = self.request_factory.put('/api/v1', data, format='json')
        # act
        response = self.view(request)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(new_first_name, old_first_name)
        self.assertEqual(new_last_name, old_last_name)
        
    def test_logged_user_changes_gender_to_non_valid_value(self):
        # arrange
        old_gender = self.user1.gender
        data = {'username':self.user1.username, 'gender':'Male'}
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_gender = self.user1.gender
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_gender, old_gender)
        self.assertFalse(new_gender=='Male')
  
        
class SignupTest(APITestCase):
    def setUp(self):
        self.view = RegisterView.as_view()
        self.fake = faker.Faker()
        
    def test_signup_with_correct_values(self):
        email = self.fake.email()
        pass_1 = self.fake.password()
        data = {'username': 'TestUser',
                'email': email,
                'password1': pass_1,
                'password2': pass_1,
                'gender': 'M',
        }
        response = self.client.post('/api/v1/registration/', data)
        user = User.objects.get(username='TestUser')
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, 'TestUser')
        self.assertEqual(user.gender, 'M')
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
        self.assertEqual(response.json()['gender'], ["Invalid input. Use 'F' for female, 'M' for male, or 'O' for other."])
    
    def test_signup_with_username_already_in_use(self):
        email_1 = self.fake.email()
        email_2 = self.fake.email()
        pass_1 = self.fake.password()
        pass_2 = self.fake.password()        
        data_1 = {'username': 'TestUser',
                  'email': email_1,
                  'password1': pass_1,
                  'password2': pass_1,
                  'gender': 'M',
        }
        data_2 = {'username': 'TestUser',
                  'email': email_2,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': 'F',
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
                  'gender': 'M',
        }
        data_2 = {'username': 'TestUser2',
                  'email': email,
                  'password1': pass_2,
                  'password2': pass_2,
                  'gender': 'F',
        }
        self.client.post('/api/v1/registration/', data_1)
        response_2 = self.client.post('/api/v1/registration/', data_2)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.json()['email'], ['A user is already registered with this e-mail address.'])

