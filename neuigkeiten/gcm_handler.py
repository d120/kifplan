
from django.conf import settings
from neuigkeiten.models import *
import requests

def send_gcm(reg_ids, data):
    payload = { 'registration_ids': reg_ids, 'data': data }
    
    url = "https://android.googleapis.com/gcm/send"
    custom_headers = {
        'Authorization': 'key=' + settings.GCM_AUTH_KEY
    }
    result = requests.post(url, json=payload, headers=custom_headers)
    print(result)

def notify(subscribers, title, body, icon, link, identifier):
    gcm_reg_ids = []
    for sub in subscribers:
        if True:#sub.notification_body == "":
            if sub.type == "GCM":
                gcm_reg_ids.append(sub.token)
        PushNotification.objects.create(subscriber=sub, title=title, body=body, icon=icon, link=link, identifier=identifier)
        
        
    send_gcm(gcm_reg_ids, { 'title': title, 'body': body, 'icon': icon, 'link': link })

