import json
import requests

def send_notification(typenot, match_id, message, playerid):
    url = f'http://127.0.0.1:8000/chat/{match_id}/'
    content = {'en' : message}
    player_ids = [playerid]
    header = {"Content-Type": "application/json; charset=utf-8"}
    heading = {'en' : f'New {typenot}'}    
    
    payload = {"app_id": '50846782-217f-457d-9b27-827330bd831c',
                "include_player_ids": player_ids,
                "contents": content,
                "heading": heading,
                "url": url}

    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
