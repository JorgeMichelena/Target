from django.test import Client
from chat.factory import MatchFactory
from channels.testing import WebsocketCommunicator
from target.routing import application
import pytest
from asgiref.sync import sync_to_async
import json
import factory
from django.test import tag
from users.models import OnesignalPlayerId
import random


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
class TestMessagesNotifications:
    def setup_method(self):
        self.client = Client()
        self.match = MatchFactory()
        self.user1 = self.match.target1.user
        self.user2 = self.match.target2.user
        text = factory.Faker('word').generate()
        self.message = json.dumps({"message": text})
        onesignal = OnesignalPlayerId(user=self.user2)
        onesignal.save()

    async def test_send_notification_when_user_is_offline(self, mocker):
        send_notification_mock = mocker.patch('chat.consumers.send_notification')
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator = auth_communicator(self.client, self.match.id)
        await communicator.connect()
        await communicator.send_to(text_data=self.message)
        await communicator.receive_from()
        await communicator.disconnect()
        assert send_notification_mock.called

    async def test_dont_send_notification_when_user_is_online(self, mocker):
        send_notification_mock = mocker.patch('chat.consumers.send_notification')
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator1 = auth_communicator(self.client, self.match.id)
        await sync_to_async(self.client.force_login)(user=self.user2)
        communicator2 = auth_communicator(self.client, self.match.id)
        await communicator1.connect()
        await communicator2.connect()
        await communicator1.send_to(text_data=self.message)
        await communicator2.disconnect()
        await communicator1.disconnect()
        assert not send_notification_mock.called

    async def test_send_a_notification_for_each_message(self, mocker):
        num_messages = random.randint(1, 20)
        send_notification_mock = mocker.patch('chat.consumers.send_notification')
        await sync_to_async(self.client.force_login)(user=self.user1)
        communicator = auth_communicator(self.client, self.match.id)
        await communicator.connect()
        for i in range(num_messages):
            await communicator.send_to(text_data=self.message)
        await communicator.disconnect()
        assert send_notification_mock.call_count == num_messages
