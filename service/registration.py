from os import error

from mongoengine.fields import BooleanField, StringField
from model.schedule import Schedule
from flask import request
import uuid
import datetime


def vaccineReg() -> BooleanField:
    s = Schedule()

    s._id = uuid.uuid4().hex
    s.nid = request.json['nid']
    s.center = request.json['center']
    s.date = datetime.datetime.today()

    # already registered??
    oldSchedule = Schedule.objects(nid=s.nid).first()
    if oldSchedule:
        return False

    s.save()
    return True
