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

    def __str__(self):
        return self.titel

    class Meta:
        ordering = ('titel',)
        verbose_name = 'Arbeitskreis'
        verbose_name_plural = 'Arbeitskreise'



class AKTermin(models.Model):
    """
    AK Termin
    """
    class Meta:
        verbose_name = _('AK-Termin')
        verbose_name_plural = _('AK-Termine')

    STATUS_CHOICES = (
        (1, _('Scheduled')),
        (2, _('Preferred')),
        (3, _('Not scheduled')),
        (4, _('Fixed (Do not autoschedule)')),
    )
    
    ak = models.ForeignKey("AK", verbose_name=_('AK'))
    kommentar = models.TextField(verbose_name=_('Kommentar'), blank=True)
    
    room = models.ForeignKey("Room", verbose_name=_('Raum'), null=True,blank=True)
    start_time = models.DateTimeField(verbose_name=_('Termin-Anfang'), null=True,blank=True)
    end_time = models.DateTimeField(verbose_name=_('Termin-Ende'), null=True,blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    
    duration = models.DurationField(verbose_name=_('Dauer'))
    constraintWeekDays = models.CharField(verbose_name=_('An einem der Tage'), max_length=255, null=True, blank=True)
    constraintBeforeTime = models.DateTimeField(verbose_name=_('Nicht vor Datum/Zeit'), max_length=255, null=True, blank=True)
    constraintAfterTime = models.DateTimeField(verbose_name=_('Nicht nach Datum/Zeit'), max_length=255, null=True, blank=True)
    constraintRooms = models.CharField(verbose_name=_('In einem der Räume'), max_length=255, null=True, blank=True)
    constraintNotParallelWithEvents = models.CharField(verbose_name=_('Nicht gleichzeitig mit Veranstaltung(en)'), max_length=255, null=True, blank=True)
    constraintForceParallelWithEvents = models.CharField(verbose_name=_('Gleichzeitig mit Veranstaltung(en)'), max_length=255, null=True, blank=True)
    constraintBeforeEvents = models.CharField(verbose_name=_('Vor Veranstaltung(en)'), max_length=255, null=True, blank=True)
    constraintAfterEvents = models.CharField(verbose_name=_('Nach Veranstaltung(en)'), max_length=255, null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(AKTermin, self).__init__(*args, **kwargs)
        self.initial_end_time = self.end_time
    
    def save(self, *args, **kwargs):
        if self.start_time == None:
            self.end_time = None
        elif self.end_time != self.initial_end_time:
            self.duration = self.end_time - self.start_time
        else:
            self.end_time = self.start_time + self.duration
        super(AKTermin, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __str__(self):
        x= "Termin "+self.get_status_display()+" "
        if self.start_time != None: x += self.start_time.strftime('%d.%m. %H:%M Uhr') + " "
        x += "(Dauer: "+str(self.duration)+") (AK: "+self.ak.titel+")"
        return x
    
class RoomAvailability(models.Model):
    """
    Information of whether a room is occupied (by another event) or reserved (for us) in a given time slot
    For KIF: AK slot
    """
    class Meta:
        verbose_name = _('Raumverfügbarkeit oder Zeitslot')
        verbose_name_plural = _('Raumverfügbarkeiten und Zeitslots')

    STATUS_CHOICES = (
        (1, _('OK (Reserved)')),
        (2, _('Blocked by other event')),
        (3, _('Should Request')),
        (4, _('Requested')),
        (5, _('Recommended Slot')),
    )

    room = models.ForeignKey("Room", verbose_name=_('Raum'))
    start_time = models.DateTimeField(verbose_name=_('Termin-Anfang'))
    end_time = models.DateTimeField(verbose_name=_('Termin-Ende'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    kommentar = models.TextField(verbose_name=_('Kommentar'), blank=True)
    mgmt_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('ID in Raumbuchungssystem'))
    
    def duration(self):
        return self.end_time - self.start_time
        
    def __str__(self):
        return self.start_time.strftime('%d.%m. %H:%M')+" "+self.room.number
    


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

    number = models.CharField(max_length=50, verbose_name=_('Nummer'), unique=True)
    type = models.CharField(max_length=2, choices=ROOM_TYPE_CHOICES, verbose_name=_('Typ'))
    has_beamer = models.BooleanField(default=False, verbose_name=_('Beamer vorhanden?'))
    capacity = models.IntegerField(verbose_name=_('Anzahl Plätze'))
    lat = models.FloatField(verbose_name=_('Latitude'), default=0, blank=True)
    lng = models.FloatField(verbose_name=_('Longitude'), default=0, blank=True)
    mgmt_source = models.CharField(max_length=20, blank=True, verbose_name=_('Verwaltet durch Raumbuchungssystem'))
    mgmt_id = models.CharField(max_length=50, blank=True, verbose_name=_('ID in Raumbuchungssystem'))
    mgmt_link = models.CharField(max_length=255, blank=True, verbose_name=_('Link zum Raumbuchungssystem'))
    mgmt_comment = models.CharField(max_length=255, blank=True)

    def get_name(self):
        return self.number
    get_name.short_description = _('Name')

    def __str__(self):
        return self.get_name()



