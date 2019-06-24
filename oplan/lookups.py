from ajax_select import LookupChannel
from ajax_select import register as register_lookupchannel
from django.db.models import Q
from django.utils.html import escape

from kiffel.models import Person
from oplan.models import Room, AKTermin


@register_lookupchannel('aktermin_lookup')
class AKTerminLookup(LookupChannel):
    model = AKTermin

    def get_query(self, q, request):
        return AKTermin.objects.filter(Q(ak__titel__icontains=q) | Q(ak__leiter__icontains=q)).order_by('kommentar')

    def get_result(self, obj):
        return str(obj)

    def format_match(self, obj):
        return u"%s" % (escape(str(obj)),)

    def format_item_desplay(self, obj):
        return u"%s" % (escape(str(obj)),)



@register_lookupchannel('room_lookup')
class RoomLookup(LookupChannel):
    model = Room

    def get_query(self, q, request):
        return Room.objects.filter(number__icontains=q).order_by('number')

    def get_result(self, obj):
        return str(obj)

    def format_match(self, obj):
        return u"%s" % (escape(str(obj)),)

    def format_item_desplay(self, obj):
        return u"%s" % (escape(str(obj)),)

@register_lookupchannel('person_lookup')
class RoomLookup(LookupChannel):
    model = Person

    def get_query(self, q, request):
        return Person.objects.filter(Q(nickname__icontains=q) | Q(vorname__icontains=q) | Q(nachname__icontains=q) ).order_by('nickname')

    def get_result(self, obj):
        return str(obj)

    def format_match(self, obj):
        return u"%s" % (escape(str(obj)),)

    def format_item_desplay(self, obj):
        return u"%s" % (escape(str(obj)),)


