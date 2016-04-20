from django.contrib import admin
from django.core.urlresolvers import reverse

from oplan.models import AK, Room, RoomOpening

@admin.register(AK)
class AKAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['titel', 'leiter', 'anzahl', 'wann', 'dauer']
    list_display_links = ['titel']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['number', 'type', 'slots_link']
    list_display_links = ['number']
    
    def slots_link(self, obj):
        return "<a href='" + reverse('oplan:roomcalendar', args=[obj.number]) + "'>Belegungen</a>"
    slots_link.allow_tags = True


@admin.register(RoomOpening)
class RoomOpeningAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['room', 'start_time', 'duration', 'status', 'kommentar']
    list_display_links = ['room', 'start_time']


