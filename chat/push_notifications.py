import json
import requests
from django.conf import settings


def send_notification(typenot, match_id, message, player_ids):
    url = f'http://127.0.0.1:8000/chat/{match_id}/'
    content = {'en': message}
    header = {"Content-Type": "application/json; charset=utf-8"}
    heading = {'en': f'New {typenot}'}
    payload = {"app_id": settings.ONESIGNAL_APP_ID,
               "include_player_ids": player_ids,
               "contents": content,
               "heading": heading,
               "url": url}
    print('Inside method')
    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
