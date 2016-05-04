from django.db import models

from django.utils.translation import ugettext_lazy as _
# Create your models here.
import datetime
from oplan.models import AK

class Beitrag(models.Model):
    """Ein Newsbeitrag."""

    class Meta:
        verbose_name = _('Beitrag')
        verbose_name_plural = _('Beiträge')
        ordering = ['published_date']


    title = models.CharField(max_length=250, verbose_name=_('Titel'))
    author = models.CharField(max_length=250, verbose_name=_('Autor'))
    content_text = models.TextField(verbose_name=_('Inhalt'))
    published_date = models.DateTimeField(verbose_name=_('Veröffentlichungsdatum'), default=datetime.datetime.now)
    
    def __str__(self):
        return self.title


class PushNewsSubscriber(models.Model):
    """
    ein Browser/Smartphone welches Pushnotifications über Änderungen an diesem AK erhält
    """
    RECEIVER_CHOICES = (
        ('GCM', 'Google Cloud Messaging'),
        ('WEBPUSH', 'Open Web Push (Firefox)')
    )
    subscribed_aks = models.ManyToManyField(AK, related_name="push_subscribers")
    subscribed_news = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=RECEIVER_CHOICES)
    token = models.CharField(max_length=255)
    
class PushNotification(models.Model):
    """
    zwischengespeicherte Pushnachricht
    """
    subscriber = models.ForeignKey(PushNewsSubscriber, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    body = models.TextField()
    icon = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    identifier = models.CharField(max_length=50)


