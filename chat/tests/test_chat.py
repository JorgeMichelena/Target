from django.test import Client
from users.factory import UserFactory
from chat.factory import MatchFactory
from channels.testing import WebsocketCommunicator
from target.routing import application
import pytest
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json
import factory
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
class TestChat:
    def setup_method(self):
        self.client = Client()
        self.match = MatchFactory()

    async def test_authorized_user_can_connect(self):
        user = self.match.target1.user
        await sync_to_async(self.client.force_login)(user=user)
        communicator = auth_communicator(self.client, self.match.id)
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_send_and_receive_message(self):
        user = self.match.target1.user
        await sync_to_async(self.client.force_login)(user=user)
        communicator = auth_communicator(self.client, self.match.id)
        await communicator.connect()
        content = factory.Faker('text').generate()
        message = json.dumps({"message": content})
        await communicator.send_to(text_data=message)
        received = await communicator.receive_from()
        response = json.loads(received)
        assert response['author'] == user.username
        assert response['message'] == content
        await communicator.disconnect()

    async def test_message_is_received_by_other_user(self):
        user_1 = self.match.target1.user
        user_2 = self.match.target2.user
        await sync_to_async(self.client.force_login)(user=user_1)
        communicator_1 = auth_communicator(self.client, self.match.id)
        await communicator_1.connect()
        await sync_to_async(self.client.force_login)(user=user_2)
        communicator_2 = auth_communicator(self.client, self.match.id)
        await communicator_2.connect()
        content_1 = factory.Faker('text').generate()
        message_1 = json.dumps({"message": content_1})
        await communicator_1.send_to(text_data=message_1)
        received_2 = await communicator_2.receive_from()
        response_2 = json.loads(received_2)
        content_2 = factory.Faker('text').generate()
        message_2 = json.dumps({"message": content_2})
        await communicator_2.send_to(text_data=message_2)
        # First call to receive_from() returns first message received by group,
        # have to call it again to get the newest message.
        await communicator_1.receive_from()
        received_1 = await communicator_1.receive_from()
        response_1 = json.loads(received_1)
        assert response_2['author'] == user_1.username
        assert response_2['message'] == content_1
        assert response_1['author'] == user_2.username
        assert response_1['message'] == content_2
        await communicator_1.disconnect()
        await communicator_2.disconnect()

    async def test_user_not_in_the_match_cant_connect(self):
        user = await database_sync_to_async(UserFactory)()
        await sync_to_async(self.client.force_login)(user=user)
        communicator = auth_communicator(self.client, self.match.id)
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_anonymous_user_cant_connect(self):
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/{self.match.id}/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()
