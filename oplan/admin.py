from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from oplan.models import AK, Room, RoomAvailability, AKTermin, Track
from django.template import RequestContext
from django.http import HttpResponseRedirect

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdminStackedInline

class AKTerminInline(AjaxSelectAdminStackedInline):
    model = AKTermin
    extra = 0
    form = make_ajax_form(AKTermin, {
            #item_code is a lookup channel
            'constraintRooms': 'room_lookup',
            'constraintNotParallelWithEvents': 'aktermin_lookup', 
            'constraintForceParallelWithEvents': 'aktermin_lookup', 
            'constraintBeforeEvents': 'aktermin_lookup', 
            'constraintAfterEvents': 'aktermin_lookup', 
             },
           show_help_text=False, help_text=None)
    fieldsets = (
      ('', {
          'fields': ('duration',)
      }),
      ('Einschränkungen für Automatische Zuordnung', {
          'classes': ('collapse',),
          'fields': ('constraintWeekDays', 'constraintBeforeTime',
        'constraintAfterTime', 'constraintRooms', 'constraintNotParallelWithEvents',
        'constraintForceParallelWithEvents', 'constraintBeforeEvents',
        'constraintAfterEvents',)
      }),
      ('Zugeordneter Termin', {
          'classes': ('collapse',),
          'fields': ('room', 'start_time', 'status', 'kommentar',)
      }),
    )   
    

@admin.register(AK)
class AKAdmin(admin.ModelAdmin):
    # admin list table view
    form = make_ajax_form(AK, {
            #item_code is a lookup channel
            'leiter_personen': 'person_lookup',
             },
           show_help_text=False, help_text=None)
    list_display = ['color_col', 'type', 'titel', 'track', 'leiter', 'anzahl', 'wann', 'dauer', 'wiki_index']
    list_filter = ['type', 'track']
    list_display_links = ['titel']
    inlines = [
        AKTerminInline,
    ]
    def color_col(self, obj):
        return "<div style='background-color: "+obj.color+"; width:16px; height:16px;'></div>"
    
    color_col.allow_tags = True
    color_col.short_description = "Farbe"
    color_col.admin_order_field = 'color'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['number', 'capacity', 'type', 'slots_link', 'visible',]
    list_editable=['visible']
    list_display_links = ['number']
    
    fieldsets = (
      ('Allgemein', {
          'fields': ('number', 'type', 'capacity', 'visible', )
      }),
      ('Ausstattung', {
          'fields': ('has_beamer',)
      }),
      ('Raumbuchungssystem', {
          'classes': ('collapse',),
          'fields': ('mgmt_source', 'mgmt_id', 'mgmt_link', 'mgmt_comment',)
      }),
      ('Koordinaten', {
          'classes': ('collapse',),
          'fields': ('lat', 'lng',),
      }),
    )
    def slots_link(self, obj):
        return "<a href='" + reverse('oplan:roomcalendar', args=[obj.number]) + "'>Gehe zum Kalendar</a>"
    slots_link.allow_tags = True
    
    actions = ['bulk_add_slots']

    class BulkAddSlotsForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        #tag = forms.ModelChoiceField(Tag.objects)

    def bulk_add_slots(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.BulkAddSlotsForm(request.POST)

            if form.is_valid():
                new_slots = [ x.split('=>') for x in request.POST['slots'].split('|') ]
                
                for room in queryset:
                    for (start,end) in new_slots:
                        RoomAvailability.objects.create(room=room, status=5,
                            start_time=start, end_time=end, kommentar="bulk")

                self.message_user(request, "Successfully added %d slots each to %d room." % (len(new_slots), len(queryset)))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.BulkAddSlotsForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        
        
        return render_to_response('oplan/bulkslotcalendar.html', {
             'rooms': queryset,
             'bulk_form': form,
             'request': request,
          }, 
          context_instance=RequestContext(request) # black magic I don't understand
        )
    bulk_add_slots.short_description = "Zeitslots zu ausgewählten Räumen hinzufügen"

@admin.register(RoomAvailability)
class RoomAvailabilityAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['status', 'room', 'start_time', 'end_time', 'kommentar']
    list_display_links = ['status', 'room', 'start_time']
    list_filter = ['status']

@admin.register(AKTermin)
class AKTerminAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['ak', 'duration', 'start_time', 'room', 'status', 'kommentar']
    list_display_links = ['ak', 'duration']
    
    actions = ['clear_termin', 'set_unscheduled']
    def clear_termin(self, request, queryset):
        for akt in queryset:
            akt.status = 3
            akt.start_time = None
            akt.end_time = None
            akt.room = None
            akt.save()
    clear_termin.short_description = "Zugeordneten Raum und Termin zurücksetzen"
    
    def set_unscheduled(self, request, queryset):
        for akt in queryset:
            akt.status = 3
            akt.save()
    set_unscheduled.short_description = 'Bei nächster automatischer Zuordnung berücksichtigen'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['color_col', 'name', 'ak_count', 'linked_aks']
    list_display_links = ['name']
    readonly_fields = ["ak_count", "linked_aks"]

    # Show a list of all AKs belonging to this track in
    def linked_aks(self, obj):
        return ", ".join([
            str(ak) for ak in obj.ak_set.all()
        ])
    linked_aks.short_description = "Zugehörige AKs"

    def color_col(self, obj):
        return "<div style='background-color: " + obj.color + "; width:16px; height:16px;'></div>"
    color_col.allow_tags = True
    color_col.short_description = "Farbe"
    color_col.admin_order_field = 'color'
