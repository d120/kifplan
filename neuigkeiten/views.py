from django.shortcuts import render
from neuigkeiten.models import *
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
import uuid

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie
def list_all(request):
    items = Beitrag.objects.all().order_by('-published_date')
    
    return render(request, 'neuigkeiten/list_all.html', { 'items' : items })
    
def list_rss(request):
    items = Beitrag.objects.all().order_by('-published_date')
    
    return render(request, 'neuigkeiten/rss.xml', { 'items' : items }, content_type="application/rss+xml")


from django.db.models.signals import post_save
from django.dispatch import receiver
from neuigkeiten import gcm_handler

@receiver(post_save, sender=Beitrag)
def created_news_post(sender, instance, created, **kwargs):
    if created: 
        subscribers = PushNewsSubscriber.objects.filter(subscribed_news=True)
        body = "News: " + instance.title
        icon = "/static/neuigkeiten/news_icon.png"
        gcm_handler.notify(subscribers, "KIF-Neuigkeiten", instance.title, icon, settings.BASE_URL+reverse('neuigkeiten:list_all'),
                "news."+str(instance.id))

from oplan.models import AKTermin
@receiver(post_save, sender=AKTermin)
def updated_aktermin(sender, instance, created, **kwargs):
    if not created:
        subscribers = instance.ak.push_subscribers.all()
        gcm_handler.notify(subscribers, "AK-Termin aktualisiert", str(instance), 
            "/static/neuigkeiten/ak_update_icon.png", settings.BASE_URL+reverse('oplan:ak_details', args=[instance.ak_id]),
            "ak."+str(instance.ak_id))


class PushRetrieveNotification(View):
    def post(self, request, *args, **kwargs):
        subs = PushNewsSubscriber.objects.get(push_uuid=request.POST['pushID'])
        my_notifications = subs.notifications.all()
        list = []
        for item in my_notifications:
            list.append({'title': item.title,'body': item.body,'icon': item.icon,'link': item.link,'identifier': item.identifier,})
        response = JsonResponse({ 'items': list })
        my_notifications.delete()
        return response

class PushNotification(View):
    def delete(self, request, *args, **kwargs):
        try:
            print(request.GET)
            item = PushNewsSubscriber.objects.get(push_uuid=request.GET['pushID'])
            item.delete()
            return JsonResponse({ 'success': True, 'deleted': True, 'was_subscribed': True })
        except PushNewsSubscriber.DoesNotExist:
            return JsonResponse({ 'success': True, 'deleted': False, 'was_subscribed': False })

    def post(self, request, *args, **kwargs):
        existed = False
        item = None
        
        if 'pushID' in request.POST:
            try:
                item = PushNewsSubscriber.objects.get(push_uuid=request.POST['pushID'])
                if 'subscription' in request.POST:
                    item.subscription = request.POST['subscription']
                    item.save()
                existed = True
            except PushNewsSubscriber.DoesNotExist:
                pass
        if item is None:
            item = PushNewsSubscriber.objects.create(
                type='WebPush', 
                push_uuid=uuid.uuid4(),
                subscription=request.POST['subscription'], 
                subscribed_news=True)
        
        if 'ak_id' in request.POST:
            ak = AK.objects.get(id=request.POST['ak_id'])
            item.subscribed_aks.add(ak)
            #TODO save?
        
        return JsonResponse({ 'success': True, 'was_subscribed': existed, 'pushID': item.push_uuid })
        
    def get(self, request, *args, **kwargs):
        try:
            item = PushNewsSubscriber.objects.get(token=request.GET['token'])
            return JsonResponse({ 'success': True, 'news_subscribed': item.news_subscribed, 'aks_subscribed':
                [x.id for x in item.ak_set.all()] })
        except PushNewsSubscriber.DoesNotExist:
            return JsonResponse({ 'success': False, 'news_subscribed': False, 'aks_subscribed': [] })


