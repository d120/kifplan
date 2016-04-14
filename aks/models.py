from django.db import models

from django.utils.translation import ugettext_lazy as _

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

    assigned_slot = models.ForeignKey("RoomOpening", verbose_name=_('Zugewiesener Zeitslot'), null=True, blank=True)

    class Meta:
        ordering = ('titel',)
        verbose_name = 'Arbeitskreis'
        verbose_name_plural = 'Arbeitskreise'


class RoomOpening(models.Model):
    """
    Information of whether a room is occupied (by another event) or reserved (for us) in a given time slot
    For KIF: AK slot
    """
    class Meta:
        verbose_name = _('AK-Slot')

    STATUS_CHOICES = (
        (1, _('OK (Reserved)')),
        (2, _('Blocked by other event')),
        (3, _('Should Request')),
        (4, _('Requested')),
    )

    room = models.ForeignKey("Room", verbose_name=_('Raum'))
    start_time = models.DateTimeField(verbose_name=_('Termin'))
    duration = models.DurationField(verbose_name=_('Dauer'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    kommentar = models.TextField(verbose_name=_('Kommentar'), blank=True)


class Room(models.Model):
    """A room which could be used during the Ophase."""

    class Meta:
        verbose_name = _('Raum')
        verbose_name_plural = _('Räume')
        ordering = ['number']
        #unique_together = ('building', 'number')

    ROOM_TYPE_CHOICES = (
        ("SR", _('Kleingruppenraum')),
        ("HS", _('Hörsaal')),
        ("PC", _('PC-Pool')),
        ("LZ", _('Lernzentrum')),
        ("SO", _('Sonstiges'))
    )

    number = models.CharField(max_length=50, verbose_name=_('Nummer'))
    type = models.CharField(max_length=2, choices=ROOM_TYPE_CHOICES, verbose_name=_('Typ'))
    has_beamer = models.BooleanField(default=False, verbose_name=_('Beamer vorhanden?'))
    capacity = models.IntegerField(verbose_name=_('Anzahl Plätze'))
    lat = models.FloatField(verbose_name=_('Latitude'), default=0, blank=True)
    lng = models.FloatField(verbose_name=_('Longitude'), default=0, blank=True)
    mgmt_source = models.CharField(max_length=20, blank=True)
    mgmt_id = models.CharField(max_length=50, blank=True)
    mgmt_link = models.CharField(max_length=255, blank=True)
    mgmt_comment = models.CharField(max_length=255, blank=True)

    def get_name(self):
        return self.number
    get_name.short_description = _('Name')

    def __str__(self):
        return self.get_name()



