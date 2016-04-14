import json, time
from .models import *
from .config import *


def slotsFromJSON(data):
    objects = json.loads(data)
    slots = []
    for obj in objects:
        slots.append(Slot(time.strptime(obj["start"], DATETIME_FORMAT), obj["room"]))
    return slots


def aksFromJSON(data):
    objects = json.loads(data)
    aks = []
    for obj in objects:
        aks.append(AK(obj["name"], obj["host"], obj["length"]))
    return aks
