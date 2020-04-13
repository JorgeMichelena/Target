from users.factory import UserFactory
from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from rest_auth.views import UserDetailsView
from factory.faker import faker
from django.urls import reverse


class EditProfileTests(APITestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.view = UserDetailsView.as_view()
        self.fname = faker.Faker().first_name()
        self.lname = faker.Faker().last_name()
        self.email = faker.Faker().email()
        self.profile_url = reverse('rest_user_details')

    def test_logged_user_changes_editable_fields(self):
        # arrange
        old_first_name = self.user1.first_name
        old_last_name = self.user1.last_name
        old_gender = self.user1.gender
        data = {'username': self.user1.username,
                'first_name': self.fname,
                'last_name': self.lname,
                'gender': User.Gender.FEMALE,
                }
        self.client.force_authenticate(self.user1)
        # act
        response = self.client.put(self.profile_url, data)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name
        new_gender = self.user1.gender

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_first_name, self.fname)
        self.assertEqual(new_last_name, self.lname)
        self.assertEqual(new_gender, User.Gender.FEMALE)
        self.assertNotEqual(new_first_name, old_first_name)
        self.assertNotEqual(new_last_name, old_last_name)
        self.assertNotEqual(new_gender, old_gender)

    def test_logged_user_changes_pk(self):
        # arrange
        old_pk = self.user1.pk
        data = {'pk': '1000',
                'username': self.user1.username,
                }
        self.client.force_authenticate(self.user1)
        # act
        response = self.client.put(self.profile_url, data)
        # assert
        new_pk = self.user1.pk
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_pk, old_pk)
        self.assertNotEqual(new_pk, '1000')

    def test_logged_user_changes_email(self):
        # arrange
        old_email = self.user1.email
        data = {'username': self.user1.username,
                'email': self.email,
                }
        self.client.force_authenticate(self.user1)
        # act
        response = self.client.put(self.profile_url, data)
        # assert
        new_email = self.user1.email

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_email, old_email)
        self.assertNotEqual(new_email, self.email)

    def test_not_logged_user_changes_editable_fields(self):
        # arrange
        old_first_name = self.user1.first_name
        old_last_name = self.user1.last_name
        data = {'username': self.user1.username,
                'first_name': self.fname,
                'last_name': self.lname,
                }
        # act
        response = self.client.put(self.profile_url, data)
        # assert
        new_first_name = self.user1.first_name
        new_last_name = self.user1.last_name

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(new_first_name, old_first_name)
        self.assertEqual(new_last_name, old_last_name)

    def test_logged_user_changes_gender_to_non_valid_value(self):
        # arrange
        old_gender = self.user1.gender
        data = {'username': self.user1.username, 'gender': 'Male'}
        self.client.force_authenticate(self.user1)
        # act
        response = self.client.put(self.profile_url, data)
        # assert
        new_gender = self.user1.gender

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(new_gender, old_gender)
        self.assertNotEqual(new_gender, 'Male')
