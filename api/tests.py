from users.factory import UserFactory
from django.test import TestCase
from api import serializers
from users.models import User
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory
from rest_auth.views import UserDetailsView

class EditProfileTests(TestCase):
        
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
                'gender':'F'}
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name
        new_gender = self.user1.gender
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_first_name, 'new_first_name')
        self.assertEqual(new_last_name, 'new_last_name')
        self.assertEqual(new_gender, 'F')
        self.assertFalse(new_first_name==old_first_name)
        self.assertFalse(new_last_name==old_last_name)
        self.assertFalse(new_gender==old_gender)
        
    
    def test_logged_user_changes_pk(self):
        # arrange
        old_pk = self.user1.pk
        data = {'pk':'1000', 'username':self.user1.username}
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_pk = self.user1.pk
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_pk, old_pk)
        self.assertFalse(new_pk=='1000')
        
    def test_logged_user_changes_email(self):
        # arrange
        old_email = self.user1.email
        data = {'username':self.user1.username, 'email':'newemail@example.com'}
        request = self.request_factory.put('/api/v1', data, format='json')
        force_authenticate(request, self.user1)
        # act
        response = self.view(request)
        # assert
        new_email = self.user1.email
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_email, old_email)
        self.assertFalse(new_email=='newemail@example.com')
    
    def test_not_logged_user_changes_editable_fields(self):
        # arrange
        old_first_name = self.user1.first_name
        old_last_name = self.user1.last_name
        data = {'username':self.user1.username, 'first_name':'new_first_name', 'last_name':'new_last_name'}
        request = self.request_factory.put('/api/v1', data, format='json')
        # act
        response = self.view(request)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name
        
        self.assertEqual(response.status_code, 403)
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
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(new_gender, old_gender)
        self.assertFalse(new_gender=='Male')
  
        
