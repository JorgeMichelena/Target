from chat.factory import MessageFactory, MatchFactory
from random import randint
from django.test import TestCase
from django.urls import reverse


class PaginatedHistoryTest(TestCase):
    def setUp(self):
        num_messages = 60
        self.match = MatchFactory()
        self.user1 = self.match.target1.user
        self.user2 = self.match.target2.user
        self.messages = []
        for i in range(num_messages):
            if i % 2 == 0:
                self.messages.append(MessageFactory(author=self.user1, chat=self.match))
            else:
                self.messages.append(MessageFactory(author=self.user2, chat=self.match))
        self.chat_url = reverse('room', kwargs={'match_id': self.match.id})

    def test_see_paginated_history_newest_20_messages_by_default(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.chat_url)
        expected_page1 = ''
        for i in range(20):
            expected_page1 += '>>' + self.messages[40+i].author.username + ':\n' + self.messages[40+i].content + '\n\n'
        self.assertEqual(response.context['chat'], expected_page1)

    def test_see_paginated_history_indicating_page(self):
        self.client.force_login(self.user1)
        response1 = self.client.get(self.chat_url + '?page=1')
        expected_page1 = ''
        for i in range(20):
            expected_page1 += '>>' + self.messages[40+i].author.username + ':\n' + self.messages[40+i].content + '\n\n'
        response2 = self.client.get(self.chat_url + '?page=2')
        expected_page2 = ''
        for i in range(20):
            expected_page2 += '>>' + self.messages[20+i].author.username + ':\n' + self.messages[20+i].content + '\n\n'
        response3 = self.client.get(self.chat_url + '?page=3')
        expected_page3 = ''
        for i in range(20):
            expected_page3 += '>>' + self.messages[i].author.username + ':\n' + self.messages[i].content + '\n\n'

        self.assertEqual(response1.context['chat'], expected_page1)
        self.assertEqual(response2.context['chat'], expected_page2)
        self.assertEqual(response3.context['chat'], expected_page3)

    def test_see_paginated_history_indicating_pages_out_of_range(self):
        self.client.force_login(self.user1)
        response1 = self.client.get(self.chat_url + f'?page={randint(-1000, 0)}')
        expected_page1 = ''
        for i in range(20):
            expected_page1 += '>>' + self.messages[40+i].author.username + ':\n' + self.messages[40+i].content + '\n\n'
        response2 = self.client.get(self.chat_url + f'?page={randint(4, 1000)}')
        expected_page2 = ''
        for i in range(20):
            expected_page2 += '>>' + self.messages[i].author.username + ':\n' + self.messages[i].content + '\n\n'

        self.assertEqual(response1.context['chat'], expected_page1)
        self.assertEqual(response2.context['chat'], expected_page2)
