from rest_framework.test import APITestCase
from rest_framework import status
from django.core import mail
from users.factory import UserFactory
from random import randint
import factory
from django.urls import reverse
from django.conf import settings


class MailAdminsTest(APITestCase):
    def setUp(self):
        self.num_admins = randint(1, 10)
        self.admins = UserFactory.create_batch(self.num_admins, is_staff=True, is_superuser=True)
        for adm in self.admins:
            adm.save()
        self.admin_mails = [admin.email for admin in self.admins]
        self.user = UserFactory()
        self.mail_url = reverse('mail_admins')

    def test_mail_is_sent_to_all_admins_when_logged_in(self):
        self.client.force_authenticate(self.user)
        message = factory.Faker('text').generate()
        subject = factory.Faker('word').generate()
        data = {'subject': subject, 'message': message}
        response = self.client.post(self.mail_url, data)
        outbox = mail.outbox
        email = outbox[0]
        email_subject = subject
        email_body = f'From: {self.user.username}\nEmail: {self.user.email}\n\n {message} \n'
        email_recipients = email.recipients()

        self.assertEqual(len(outbox), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(email_subject, email.subject)
        self.assertEqual(settings.EMAIL_HOST_USER, email.from_email)
        self.assertEqual(email_body, email.body)
        self.assertCountEqual(email_recipients, self.admin_mails)

    def test_mail_is_sent_to_all_admins_when_not_logged_in(self):
        message = factory.Faker('text').generate()
        subject = factory.Faker('word').generate()
        data = {'subject': subject, 'message': message}
        response = self.client.post(self.mail_url, data)
        outbox = mail.outbox
        email = outbox[0]
        email_subject = subject
        email_body = f'From: Anonymous user\nEmail: No e-mail\n\n {message} \n'
        email_recipients = email.recipients()
        self.assertEqual(len(outbox), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(email_subject, email.subject)
        self.assertEqual(settings.EMAIL_HOST_USER, email.from_email)
        self.assertEqual(email_body, email.body)
        self.assertCountEqual(email_recipients, self.admin_mails)

    def test_mail_is_not_sent_when_body_is_blank(self):
        message = ''
        subject = factory.Faker('word').generate()
        data = {'subject': subject, 'message': message}
        response = self.client.post(self.mail_url, data)
        outbox = mail.outbox
        self.assertEqual(len(outbox), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], ['This field may not be blank.'])

    def test_mail_is_not_sent_when_subject_is_blank(self):
        message = factory.Faker('text').generate()
        subject = ''
        data = {'subject': subject, 'message': message}
        response = self.client.post(self.mail_url, data)
        outbox = mail.outbox
        self.assertEqual(len(outbox), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['subject'], ['This field may not be blank.'])
