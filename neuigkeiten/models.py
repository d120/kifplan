from django.db import models

# Create your models here.


class Beitrag(models.Model):
    """Ein Newsbeitrag."""

    class Meta:
        verbose_name = _('Beitrag')
        verbose_name_plural = _('Beiträge')
        ordering = ['publish_date']


    title = models.CharField(max_length=250, verbose_name=_('Titel'))
    author = models.CharField(max_length=250, verbose_name=_('Autor'))
    content_text = models.TextField(verbose_name=_('Inhalt'))
    published_date = models.DateTimeField(verbose_name=_('Veröffentlichungsdatum'), auto_now_add=True)
    
    def __str__(self):
        return self.title


