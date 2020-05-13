from django.test import Client
from users.factory import UserFactory
from chat.factory import MatchFactory
from channels.testing import WebsocketCommunicator
from target.routing import application
import pytest
from asgiref.sync import sync_to_async
import json
import factory
from django.urls import reverse
from django.test import tag


def auth_communicator(client, match_id):
    return WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/{match_id}/',
            headers=[(
                b'cookie',
                f'sessionid={client.cookies["sessionid"].value}'.encode('ascii')
            )]
        )


@tag('pytest')
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestUnreadMessages:
    def setup_method(self):
        self.client = Client()
        self.match = MatchFactory()
        self.user1 = self.match.target1.user
        self.user2 = self.match.target2.user
        self.user3 = UserFactory()
        self.text1 = factory.Faker('word').generate()
        self.text2 = factory.Faker('word').generate()
        self.text3 = factory.Faker('word').generate()
        self.msg1 = json.dumps({"message": self.text1})
        self.msg2 = json.dumps({"message": self.text2})
        self.msg3 = json.dumps({"message": self.text3})
        self.match_url = reverse('match-detail', kwargs={'pk': self.match.pk})

    async def test_see_unread_messages_before_connecting(self):
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator = auth_communicator(self.client, self.match.id)
        await communicator.connect()
        await communicator.send_to(text_data=self.msg1)
        await communicator.send_to(text_data=self.msg2)
        await communicator.send_to(text_data=self.msg3)
        await communicator.disconnect()
        await sync_to_async(self.client.force_login)(self.user2)
        response = await sync_to_async(self.client.get)(self.match_url)

        assert response.json()['unread_messages'] == 3
        assert response.json()['last_message'] == self.text3

    async def test_see_unread_messages_after_connecting(self):
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator1 = auth_communicator(self.client, self.match.id)
        await communicator1.connect()
        await communicator1.send_to(text_data=self.msg1)
        await communicator1.send_to(text_data=self.msg2)
        await communicator1.send_to(text_data=self.msg3)
        await communicator1.disconnect()
        await sync_to_async(self.client.force_login)(self.user2)
        communicator2 = auth_communicator(self.client, self.match.id)
        await communicator2.connect()
        await communicator2.disconnect()
        response = await sync_to_async(self.client.get)(self.match_url)

        assert response.json()['unread_messages'] == 0
        assert response.json()['last_message'] == ''

    async def test_number_of_unread_messages_depends_of_the_user(self):
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator = auth_communicator(self.client, self.match.id)
        await communicator.connect()
        await communicator.send_to(text_data=self.msg1)
        await communicator.send_to(text_data=self.msg2)
        await communicator.send_to(text_data=self.msg3)
        await communicator.disconnect()
        response_user1 = await sync_to_async(self.client.get)(self.match_url)
        await sync_to_async(self.client.force_login)(user=self.user2)
        response_user2 = await sync_to_async(self.client.get)(self.match_url)

        assert response_user1.json()['unread_messages'] == 0
        assert response_user1.json()['last_message'] == self.text3
        assert response_user2.json()['unread_messages'] == 3
        assert response_user2.json()['last_message'] == self.text3
