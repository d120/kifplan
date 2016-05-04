from django.shortcuts import render
from neuigkeiten.models import *
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse

# Create your views here.
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
        subs = PushNewsSubscriber.objects.get(token=request.POST['token'])
        my_notifications = subs.notifications.all()
        list = []
        for item in my_notifications:
            list.append({'title': item.title,'body': item.body,'icon': item.icon,'link': item.link,'identifier': item.identifier,})
        response = JsonResponse({ 'items': list })
        my_notifications.delete()
        return response

class PushNotification(View):
    def post(self, request, *args, **kwargs):
        existed = False
        try:
            if 'oldtoken' in request.POST:
                item = PushNewsSubscriber.objects.get(token=request.POST['oldtoken'])
                item.token = request.POST['token']
                item.save()
            else:
                item = PushNewsSubscriber.objects.get(token=request.POST['token'])
                if 'delete' in request.POST:
                    item.delete()
                    return JsonResponse({ 'success': True, 'deleted': True, 'was_subscribed': True })
            existed = True
        except PushNewsSubscriber.DoesNotExist:
            if 'delete' in request.POST:
                return JsonResponse({ 'success': True, 'deleted': False, 'was_subscribed': False })
            
            item = PushNewsSubscriber.objects.create(type='GCM', token=request.POST['token'], subscribed_news=True)
        
        if 'ak_id' in request.POST:
            ak = AK.objects.get(id=request.POST['ak_id'])
            item.subscribed_aks.add(ak)
        
        return JsonResponse({ 'success': True, 'was_subscribed': existed })
        
    def get(self, request, *args, **kwargs):
        try:
            item = PushNewsSubscriber.objects.get(token=request.GET['token'])
            return JsonResponse({ 'success': True, 'news_subscribed': item.news_subscribed, 'aks_subscribed':
                [x.id for x in item.ak_set.all()] })
        except PushNewsSubscriber.DoesNotExist:
            return JsonResponse({ 'success': False, 'news_subscribed': False, 'aks_subscribed': [] })


