
from django.conf import settings
from neuigkeiten.models import *
from pywebpush import webpush
import json

def notify(subscribers, title, body, icon, link, identifier):
    data_obj = { 'title': title, 'body': body, 'icon': icon, 'link': link }
    data = json.dumps(data_obj).encode("utf-8")
    print("webPush notify",data)
    for sub in subscribers:
        print("subscriber",sub)
        try:
            if True:#sub.notification_body == "":
                sub_info = json.loads(sub.subscription)
                print("sub_info",sub_info)
                res=webpush(sub_info, data)
                print(res)
            PushNotification.objects.create(subscriber=sub, title=title, body=body, icon=icon, link=link, identifier=identifier)
        except Exception as ex:
            print("Notification failed for subscriber")
            print(ex)

