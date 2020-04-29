from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from django.test import Client
import factory
from users.factory import UserFactory
from chat.factory import MatchFactory
from django.urls import reverse


class UnreadMessagesTests(ChannelsLiveServerTestCase):
    serve_static = True

    def setUp(self):
        super().setUpClass()
        self.client = Client()
        self.match = MatchFactory()
        self.user1 = self.match.target1.user
        self.user2 = self.match.target2.user
        self.user3 = UserFactory()
        self.text1 = factory.Faker('word').generate()
        self.text2 = factory.Faker('word').generate()
        self.text3 = factory.Faker('word').generate()
        self.match_url = reverse('match-detail', kwargs={'pk': self.match.pk})
        # The directory in wich chromedriver's binary is in must be added to $PATH
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_see_unread_messages_before_entering_chatroom(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )

        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(self.match_url)
        self.assertEqual(response.json()['unread_messages'], 3)
        self.assertEqual(response.json()['last_message'], self.text3)

    def test_see_unread_messages_after_entering_chatroom(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self.client.logout()
        self._authenticate_user(self.user2)
        self._enter_chat_room(self.match.id)
        response = self.client.get(self.match_url)
        self.assertEqual(response.json()['unread_messages'], 0)
        self.assertEqual(response.json()['last_message'], '')

    def test_number_of_unread_messages_depends_of_the_user(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )

        response_user1 = self.client.get(self.match_url)

        self.client.logout()
        self.client.force_login(self.user2)
        response_user2 = self.client.get(self.match_url)

        self.assertEqual(response_user1.json()['unread_messages'], 0)
        self.assertEqual(response_user1.json()['last_message'], self.text3)
        self.assertEqual(response_user2.json()['unread_messages'], 3)
        self.assertEqual(response_user2.json()['last_message'], self.text3)

    # Methods used in testing
    def _enter_chat_room(self, match_id):
        self.driver.get(self.live_server_url + reverse('room', kwargs={'match_id': match_id}))

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        input_text = self.driver.find_element_by_id('chat-message-input')
        submit = self.driver.find_element_by_id('chat-message-submit')
        input_text.send_keys(message)
        submit.click()

    def _authenticate_user(self, user):
        self.client.force_login(user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + reverse('rest_login'))
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh()

    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
