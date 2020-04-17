from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from django.test import Client
from chat.factory import MatchFactory
from users.factory import UserFactory
from rest_framework import status
from django.urls import reverse


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.match = MatchFactory()
        self.user1 = self.match.target1.user
        self.user2 = self.match.target2.user
        self.user3 = UserFactory()

        # The directory in wich chromedriver's binary is in must be added to $PATH
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_chat_message_posted_then_seen_in_different_windows_same_user_logged(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)
        self._open_new_window()
        self._enter_chat_room(self.match.id)

        self._switch_to_window(0)
        self._post_message('hello')
        WebDriverWait(self.driver, 2).until(
            lambda _:
            'hello' in self._chat_log_value(),
            'Message was not received by window 1 from window 1'
                                            )
        self._switch_to_window(1)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            'hello' in self._chat_log_value(),
            'Message was not received by window 2 from window 1'
                                            )

    def test_when_chat_message_posted_then_seen_by_the_other_user(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)
        self._post_message('hello')
        self.client.logout()

        self._authenticate_user(self.user2)
        self._enter_chat_room(self.match.id)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            'hello' in self._chat_log_value(),
            'Message was not received by window 2 from window 1'
                                            )

        self._post_message('world')
        self.client.logout()

        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)
        WebDriverWait(self.driver, 2).until(
            lambda _:
            'world' in self._chat_log_value(),
            'Message was not received by window 1 from window 2'
                                            )

    def test_when_chat_message_posted_cannot_be_seen_by_users_not_in_the_match(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match.id)
        self._post_message('hello')
        self.client.logout()
        self.client.force_login(self.user3)
        chat_suffix = reverse('room', kwargs={'match_id': self.match.id})
        response = self.client.get(self.live_server_url + chat_suffix)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        ActionChains(self.driver).send_keys(message + '\n').perform()

    def _authenticate_user(self, user):
        self.client.force_login(user)
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/api/v1/')
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh()

    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
