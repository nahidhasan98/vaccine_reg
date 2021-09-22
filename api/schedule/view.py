from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime, timedelta
from sqlalchemy import func
from marshmallow import ValidationError
from api.schedule.model import ScheduleModel, ScheduleSchema
from core.db import db


class HelperService():
    # getting next available free slot/date for registration for a specific center
    def getNextAvailableSlot(self, center, dailyLimit):
        today = datetime.today().date()

        rows = db.session.query(ScheduleModel.date, func.count(ScheduleModel.date).label('total')) \
            .group_by(ScheduleModel.date) \
            .filter(ScheduleModel.center == center, ScheduleModel.date > today) \
            .order_by(ScheduleModel.date.asc())

        # safely assuming slot
        if rows.count() > 0:
            # last registered day + 1
            gotSlot = rows[rows.count()-1].date+timedelta(days=1)
        else:
            # if no registration done in this center
            gotSlot = today+timedelta(days=1)

        # checking if any slot available between total registartion date range
        curr = today+timedelta(days=1)
        for row in rows:
            if row.date != curr:
                gotSlot = curr
                break
            elif row.total < dailyLimit:
                gotSlot = row.date
                break
            else:
                curr += timedelta(days=1)

        return gotSlot

    # checking available free slot for registration for a specific center and date
    def hasSlot(self, center, date, dailyLimit):
        counter = ScheduleModel.query.filter_by(
            center=center, date=date).count()

        if counter < dailyLimit:
            return True

        return False

    # checking if provided nid is already registered or not
    def alreadyRegistered(self, nid):
        exist = ScheduleModel.query.filter_by(nid=nid).first()

        if exist:
            return True

        return False


class ScheduleService(HelperService):
    # daily registration limit
    __dailyLimit = 3

    # function for registration
    def addSchedule(self, nid, center, date):
        s = ScheduleModel(
            nid=nid,
            center=center,
            date=date
        )

        # already registered??
        if self.alreadyRegistered(nid):
            return None, "this nid already registered"

        # taking care of date
        if date:
            if not self.hasSlot(center, date, self.__dailyLimit):
                freeSlot = self.getNextAvailableSlot(center, self.__dailyLimit)
                return None, "no available slot on " + str(date) + ", next available free slot on " + str(freeSlot)
        else:
            s.date = self.getNextAvailableSlot(center, self.__dailyLimit)

        db.session.add(s)
        db.session.commit()
        return s, None

    # function for getting schedule on a specific date
    def getSchedule(self, date):
        err = None
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            err = 'invalid date format. required format is: 2018-12-31'

        # querying from db
        rows = ScheduleModel.query.filter_by(date=date)

        return rows, err


class Schedule(Resource):
    def get(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        requestDate = request.json.get('date')

        # creating object for GetSchedule class
        object = ScheduleService()
        result, err = object.getSchedule(requestDate)

        if err != None:
            return {"err": err}, 400

        # serializing object to native Python data types according to the Schema's fields
        schema = ScheduleSchema(many=True)
        schedules = schema.dump(result)

        return jsonify({
            "msg": "success",
            "date": requestDate,
            "schedules": schedules
        })

    def post(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        requestData = request.get_json()

        try:
            # deserializing data structure to an object defined by the Schema's fields
            schema = ScheduleSchema()
            schedule = schema.load(requestData)
        except ValidationError as err:
            return {"err": err.messages}, 400

        # creating object for Registration class
        object = ScheduleService()
        result, err = object.addSchedule(
            schedule.nid, schedule.center, schedule.date)

        if err != None:
            return {"err": err}, 400

        # serializing object to native Python data types according to the Schema's fields
        addedSchedule = schema.dump(result)

        return jsonify({
            "msg": "registration successful",
            "schedule": addedSchedule
        })
