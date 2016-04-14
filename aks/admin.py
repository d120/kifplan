from django.contrib import admin

from aks.models import AK, Room, RoomOpening

@admin.register(AK)
class AKAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['titel', 'leiter', 'anzahl', 'wann', 'dauer']
    list_display_links = ['titel']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['number', 'type']
    list_display_links = ['number']


@admin.register(RoomOpening)
class RoomOpeningAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['room', 'start_time', 'duration', 'status', 'kommentar']
    list_display_links = ['room', 'start_time']


