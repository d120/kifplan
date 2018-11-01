from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from kiffel.models import Person


class Settings(models.Model):
    """Configuration for Plan App."""

    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"

    ak_start_day = models.DateField(verbose_name="Erster AK-Tag")
    ak_end_day = models.DateField(verbose_name="Letzer AK-Tag")
    ak_start_hour = models.TimeField(verbose_name="Beginn der AKs (Uhrzeit)")
    ak_end_hour = models.TimeField(verbose_name="Ende der AKs (Uhrzeit)")

    def __str__(self):
        return "Einstellungen Plan-App"

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if Settings.objects.count() > 0 and self.id != Settings.objects.get().id:
            raise ValidationError(_("Es ist nur sinnvoll und möglich eine Instanz des Einstellungsobjekts anzulegen."))

    @staticmethod
    def instance():
        try:
            return Settings.objects.get()
        except Settings.DoesNotExist:
            return None


class Track(models.Model):
    """ ein Track bündelt eine Reihe von Arbeitskreisen mit ähnlichem Thema """
    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"

    name = models.CharField(max_length=200, null=False, blank=False)
    color = models.CharField(max_length=10, default='#34495e', verbose_name="Farbe")

    def ak_count(self):
        return self.ak_set.count()
    ak_count.short_description = "Anzahl zugehöriger AKs"

    def __str__(self):
        return self.name


class AK(models.Model):
    """ repräsentiert einen Arbeitskreis der KIF """

    # Stammdaten
    titel = models.CharField(max_length=400, null=True, blank=True, verbose_name="Bezeichnung")
    type = models.CharField(max_length=50, null=True, blank=True, verbose_name="Art")
    leiter = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wer macht's?")
    anzahl = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wie viele?")
    wann = models.CharField(max_length=400, null=True, blank=True, verbose_name="Wann?")
    dauer = models.CharField(max_length=400, null=True, blank=True, verbose_name="Dauer?")
    beschreibung = models.TextField(null=True, blank=True)
    wiki_link = models.CharField(max_length=100, null=True, blank=True, verbose_name="Link zur Wikiseite")
    internal_color = models.CharField(max_length=10, default='#ff00ff', verbose_name="Farbe")
    wiki_index = models.IntegerField(default=0)
    
    interesse = models.IntegerField(default=0)
    
    leiter_personen = models.ManyToManyField(Person, blank=True, related_name="leitet_aks", help_text="Werden bei Zuteilung berücksichtigt")

    beamer = models.BooleanField(default=False, verbose_name=_('Beamer benötigt?'))
    internet = models.BooleanField(default=False, verbose_name=_('Internet benötigt?'))
    whiteboard = models.BooleanField(default=False, verbose_name=_('Whiteboard oder Tafel benötigt?'))
    reso = models.BooleanField(default=False, verbose_name=_('Absicht auf eine Resolution?'))

    track = models.ForeignKey(Track, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.titel

    @property
    def color(self):
        if self.track is not None:
            return self.track.color
        return self.internal_color

    class Meta:
        ordering = ('type', 'track', 'titel',)
        verbose_name = 'Arbeitskreis'
        verbose_name_plural = 'Arbeitskreise'

def fmt_or_msg(time):
    if time:
        return timezone.localtime(time).strftime('%a %H:%M')
    else:
        return "(not assigned yet)"

class ConstraintWeekDays:
    def __init__(self, weekdays):
        self.weekdays = weekdays.lower().split('|')
    def check(self, termin):
        return (not termin.start_time) or timezone.localtime(termin.start_time).strftime('%a')[0:2].lower() in self.weekdays
    def json(self):
        return ('WEEKDAY', self.weekdays, 'Weekday '+ (' or '.join(wd.title() for wd in self.weekdays)))
class ConstraintRooms:
    def __init__(self, rooms):
        self.rooms = rooms
    def check(self, termin):
        return not termin.room or any(termin.room.id == r.id for r in self.rooms)
    def json(self):
        return ('ROOMS', [x.id for x in self.rooms], 'In room '+ ' or '.join(x.number for x in self.rooms) )
class ConstraintBeforeDt:
    def __init__(self, dt):
        self.dt = dt
    def check(self, termin):
        return not termin.start_time or termin.start_time < self.dt
    def json(self):
        return ('BEFORE_DT', self.dt, 'Before '+timezone.localtime(self.dt).strftime('%a %H:%M'))
class ConstraintAfterDt:
    def __init__(self, dt):
        self.dt = dt
    def check(self, termin):
        return not termin.start_time or  termin.start_time > self.dt
    def json(self):
        return ('AFTER_DT', self.dt, 'After '+timezone.localtime(self.dt).strftime('%a %H:%M'))
class ConstraintNotParallel:
    def __init__(self, other_event):
        self.other_event = other_event
    def check(self, termin):
        return (not termin.end_time or not self.other_event.start_time or not termin.start_time or not self.other_event.end_time
            or termin.end_time <= self.other_event.start_time or termin.start_time >= self.other_event.end_time)
    def json(self):
        return ('NOT_PARALLEL', self.other_event.id, 
                'NOT overlapping with '+str(self.other_event))
class ConstraintNotParallelBecauseLeiter(ConstraintNotParallel):
    def __init__(self, other_event, leiter):
        self.other_event = other_event
        self.leiter = leiter
    def json(self):
        return ('NOT_PARALLEL', self.other_event.id, 
                'NOT overlapping with '+str(self.other_event)+ ' because same leiter '+self.leiter)
class ConstraintForceParallel:
    def __init__(self, other_event):
        self.other_event = other_event
    def check(self, termin):
        return (not termin.start_time or not self.other_event.start_time
            or termin.start_time == self.other_event.start_time)
    def json(self):
        return ('FORCE_PARALLEL', self.other_event.id, 'At the same time as '+str(self.other_event))
class ConstraintBeforeEvent:
    def __init__(self, other_event):
        self.other_event = other_event
    def check(self, termin):
        return (not termin.end_time or not self.other_event.start_time
                or termin.end_time <= self.other_event.start_time)
    def json(self):
        return ('BEFORE', self.other_event.id, 'Before '+str(self.other_event))
class ConstraintAfterEvent:
    def __init__(self, other_event):
        self.other_event = other_event
    def check(self, termin):
        return (not termin.start_time or not self.other_event.end_time
                or termin.start_time >= self.other_event.end_time)
    def json(self):
        return ('AFTER', self.other_event.id, 'After '+str(self.other_event.ak.titel))


class AKTermin(models.Model):
    """
    AK Termin
    """
    class Meta:
        verbose_name = _('AK-Termin')
        verbose_name_plural = _('AK-Termine')
        #ordering = ('ak.titel',)

    STATUS_CHOICES = (
        (1, _('Scheduled')),
        #(2, _('Preferred')),
        (3, _('Not scheduled')),
        (4, _('Fixed (Do not autoschedule)')),
    )
    
    ak = models.ForeignKey("AK", verbose_name=_('AK'))
    kommentar = models.TextField(verbose_name=_('Kommentar'), blank=True)
    
    room = models.ForeignKey("Room", verbose_name=_('Raum'), null=True,blank=True)
    start_time = models.DateTimeField(verbose_name=_('Termin-Anfang'), null=True,blank=True)
    end_time = models.DateTimeField(verbose_name=_('Termin-Ende'), null=True,blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=3)
    
    last_modified = models.DateTimeField(verbose_name=_('Zuletzt geändert'), auto_now=True)
    last_highlighted = models.DateTimeField(verbose_name=_('Änderungshighlight'), null=True, blank=True)
    
    duration = models.DurationField(verbose_name=_('Dauer'))
    constraintWeekDays = models.CharField(verbose_name=_('An einem der Tage'), max_length=255, null=True, blank=True)
    constraintBeforeTime = models.DateTimeField(verbose_name=_('Nicht nach Datum/Zeit'), max_length=255, null=True, blank=True)
    constraintAfterTime = models.DateTimeField(verbose_name=_('Nicht vor Datum/Zeit'), max_length=255, null=True, blank=True)
    constraintRooms = models.ManyToManyField('Room', verbose_name=_('In einem der Räume'), related_name='aktermin_constraint_room', blank=True, 
        help_text="Gib eine Raumnummer ein, um festzulegen, dass der AK nur in ausgewählten Räumen stattfinden kann.")
    constraintNotParallelWithEvents = models.ManyToManyField('AKTermin', related_name='constraint_not_parallel_with_this', verbose_name=_('Nicht gleichzeitig mit Veranstaltung(en)'), blank=True,
        help_text="Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin nicht gleichzeitig mit den ausgewählten AK-Terminen stattfinden kann")
    constraintForceParallelWithEvents = models.ManyToManyField('AKTermin', related_name='constraint_force_parallel_with_this', verbose_name=_('Gleichzeitig mit Veranstaltung(en)'), blank=True,
        help_text="Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin gleichzeitig mit den ausgewählten AK-Terminen stattfinden muss")
    constraintBeforeEvents = models.ManyToManyField('AKTermin', related_name='constraint_must_be_before_this', verbose_name=_('Vor Veranstaltung(en)'), blank=True,
        help_text="Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin vor den ausgewählten AK-Terminen stattfinden muss")
    constraintAfterEvents = models.ManyToManyField('AKTermin', related_name='constraint_must_be_after_this', verbose_name=_('Nach Veranstaltung(en)'), blank=True,
        help_text="Suche nach einem AK-Termin, um festzulegen, dass der AK-Termin nach den ausgewählten AK-Terminen stattfinden muss")
    
    def get_constraints(self):
        ctr = []
        if self.constraintWeekDays:
            ctr.append( ConstraintWeekDays(self.constraintWeekDays) )
        if self.constraintRooms.count() > 0:
            ctr.append( ConstraintRooms(self.constraintRooms.all()) )
        if self.constraintBeforeTime:
            ctr.append( ConstraintBeforeDt(self.constraintBeforeTime) )
        if self.constraintAfterTime:
            ctr.append( ConstraintAfterDt(self.constraintAfterTime) )
        for evt in self.constraintNotParallelWithEvents.all():
            ctr.append( ConstraintNotParallel(evt) )
        for evt in self.constraintForceParallelWithEvents.all():
            ctr.append( ConstraintForceParallel(evt) )
        for evt in self.constraintBeforeEvents.all():
            ctr.append( ConstraintBeforeEvent(evt) )
        for evt in self.constraintAfterEvents.all():
            ctr.append( ConstraintAfterEvent(evt) )
        for people in self.ak.leiter_personen.all():
            for other in people.leitet_aks.all():
                if other != self.ak:
                    for other_termin in other.aktermin_set.all():
                        ctr.append( ConstraintNotParallelBecauseLeiter(other_termin, people.nickname) )
        return ctr
    
    def get_reverse_constraints(self):
        ctr = []
        for evt in self.constraint_not_parallel_with_this.all():
            ctr.append((evt, ConstraintNotParallel(self) ))
        for evt in self.constraint_force_parallel_with_this.all():
            ctr.append((evt, constraintForceParallelWithEvents(self) ))
        for evt in self.constraint_must_be_before_this.all():
            ctr.append((evt, ConstraintBeforeEvent(self) ))
        for evt in self.constraint_must_be_after_this.all():
            ctr.append((evt, ConstraintAfterEvent(self) ))
        return ctr
    
    def check_constraints(self):
        ok, fail, reverse_fail = [], [], []
        for ctr in self.get_constraints():
            if ctr.check(self):
                ok.append(ctr.json())
            else:
                fail.append(ctr.json())
        for other, ctr in self.get_reverse_constraints():
            if not ctr.check(other):
                reverse_fail.append((str(other), ctr.json()))
        return ok, fail, reverse_fail
    
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
        x= self.ak.titel + " <- Termin "+self.get_status_display()+" "
        if self.start_time != None: x += timezone.localtime(self.start_time).strftime('%d.%m. %H:%M Uhr') + " "
        x += "(Dauer: "+str(self.duration)+")"
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
    
    visible = models.BooleanField(default=False, verbose_name=_('Im Frontend sichtbar'))
    
    def get_name(self):
        return self.number
    get_name.short_description = _('Name')

    def __str__(self):
        return self.get_name()



