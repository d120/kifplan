from django.db import models

class AK(models.Model):
    """ repräsentiert einen Arbeitkreis der KIF """

    # Stammdaten
    titel = models.CharField(max_length=400, null=True, blank=True, verbose_name="Bezeichnung")
    leiter = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wer macht's?")
    anzahl = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wie viele?")
    wann = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wann?")
    dauer = models.CharField(max_length=400, null=True, blank=True, verbose_name="Dauer?")
    beschreibung = models.TextField(null=True, blank=True)
    wiki_link = models.CharField(max_length=100, null=True, blank=True, verbose_name="Link zur Wikiseite")

    class Meta:
        ordering = ('titel',)
        verbose_name = 'Arbeitskreis'
        verbose_name_plural = 'Arbeitskreise'
