
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from django.test import Client
from chat.models import Match
from targets.factory import TopicFactory, TargetFactory
from users.models import User
from targets.models import Topic, Target
from rest_framework import status
from time import sleep
import factory


class UnreadMessagesTests(ChannelsLiveServerTestCase):
    serve_static = True 
    def setUp(self):
        super().setUpClass()
        self.client = Client()
        #define data to make users and then register them
        data1 = { 
            'username': 'usuario1',
            'email': 'usuario1@example.com',
            'password1': 'test1234password',
            'password2': 'test1234password',
            'gender': User.MALE
        }
        data2 = { 
            'username': 'usuario2',
            'email': 'usuario2@example.com',
            'password1': 'test1234password',
            'password2': 'test1234password',
            'gender': User.MALE
        }

        self.client.post('/api/v1/registration/', data1)
        self.client.post('/api/v1/registration/', data2)

        #Save models in database
        self.users = User.objects.all()
        self.user1 = self.users[0]
        self.user2 = self.users[1]
        self.topic = TopicFactory()
        self.target1 = TargetFactory(user=self.user1, topic=self.topic)
        self.target2 = TargetFactory(user=self.user2, topic=self.topic, location=self.target1.location)
        self.match1 = Match(target1=self.target1, target2=self.target2)
        self.topic.save()
        self.user1.save()
        self.user2.save()
        self.target1.save()
        self.target2.save()
        self.match1.save()

        self.text1 = factory.Faker('word').generate()
        self.text2 = factory.Faker('word').generate()
        self.text3 = factory.Faker('word').generate()


        #The directory in wich chromedriver's binary is in must be added to $PATH
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()
        

    def test_see_unread_messages_before_entering_chatroom(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match1.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        
        self.client.logout()
        self.client.login(username=self.user2.username, password='test1234password')
        response = self.client.get(f'/api/v1/matches/{self.match1.id}/')
        self.assertEqual(response.json()['unread_messages'], 3)
        self.assertEqual(response.json()['last_message'], self.text3)

    def test_see_unread_messages_after_entering_chatroom(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match1.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        
        self.client.logout()
        self._authenticate_user(self.user2)
        self._enter_chat_room(self.match1.id)
        #Need a little delay, otherwise I get a response before messages can update their date_seen field
        sleep(0.1)
        response = self.client.get(f'/api/v1/matches/{self.match1.id}/')
        
        self.assertEqual(response.json()['unread_messages'], 0)
        self.assertEqual(response.json()['last_message'], '')

    def test_number_of_unread_messages_depends_of_the_user(self):
        self._authenticate_user(self.user1)
        self._enter_chat_room(self.match1.id)

        self._switch_to_window(0)
        self._post_message(self.text1)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text1 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text2)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text2 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        self._post_message(self.text3)
        WebDriverWait(self.driver, 2).until(lambda _:
            self.text3 in self._chat_log_value(),
            'Message was not received by window 1 from window 1')
        
        response_user1 = self.client.get(f'/api/v1/matches/{self.match1.id}/')
        
        self.client.logout()
        self.client.login(username=self.user2.username, password='test1234password')
        response_user2 = self.client.get(f'/api/v1/matches/{self.match1.id}/')
        
        self.assertEqual(response_user1.json()['unread_messages'], 0)
        self.assertEqual(response_user1.json()['last_message'], self.text3)
        self.assertEqual(response_user2.json()['unread_messages'], 3)
        self.assertEqual(response_user2.json()['last_message'], self.text3)
        

    #Methods used in testing
    def _enter_chat_room(self, match_id):
        self.driver.get(self.live_server_url + f'/chat/{match_id}')

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
        self.client.login(username=user.username, password='test1234password')
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/api/v1/')
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh()

    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
