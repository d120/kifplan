from django.core.management.base import BaseCommand, CommandError
from oplan.models import AKTermin, Room, RoomAvailability
from oplan.darwin.models import AK as DarwinAK, Slot as DarwinSlot
from oplan.darwin.evolution import find_solution
from oplan.darwin.constraints import *
import math

class Command(BaseCommand):
    help = 'Ordnet alle nicht zugeordneten AK-Termine zu'

    def add_arguments(self, parser):
        parser.add_argument('--iterations', type=int, default=100)
        parser.add_argument('--fertility', type=int, default=4)
        parser.add_argument('--mutations', type=int, default=1)
        

    def handle(self, *args, **options):
        termine = AKTermin.objects.filter(status=3)  # 3 => Unscheduled
        all_slots = RoomAvailability.objects.filter(status=5).order_by('start_time')  # 5 => AKSlot
        
        slots = []
        for slot in all_slots:
            if AKTermin.objects.filter(status__in=(1,4), start_time=slot.start_time, room=slot.room).count() == 0:
                sss = DarwinSlot(start=slot.start_time, room=slot.room.number)
                sss.django_room = slot.room
                slots.append(sss)
                print('  slot: ',slot.start_time,slot.room.number)
        
        aks = []
        for termin in termine:
            ak = DarwinAK(termin.ak.titel, termin.ak.leiter, 
                math.ceil(termin.duration.total_seconds() / (60*120)))
            if termin.constraintWeekDays:
                ak.constraints.append(AKWantsWeekdayConstraint(ak, termin.constraintWeekDays))
            if termin.constraintBeforeTime:
                ak.constraints.append(AKBeforeDateTimeConstraint(ak, termin.constraintBeforeTime))
            if termin.constraintAfterTime:
                ak.constraints.append(AKAfterDateTimeConstraint(ak, termin.constraintAfterTime))
            ak.django_ak_termin = termin
            aks.append(ak)
        
        # calculate solution
        solution, fitness, messages = find_solution(slots, aks, options['iterations'], options['fertility'], options['mutations'])

        # print out result
        if len(messages) > 0:
            print("\nSome problems exist with this solution:")
            for message in messages:
                print(message)
        print()
        #print(solution)
        for ak, slot in solution.schedule:
            if ak and slot:
                ak.django_ak_termin.start_time = slot.start
                ak.django_ak_termin.end_time = slot.start + ak.django_ak_termin.duration
                ak.django_ak_termin.room = slot.django_room
                ak.django_ak_termin.save()
        
        
