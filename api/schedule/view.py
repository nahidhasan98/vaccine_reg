from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime, timedelta
from sqlalchemy import func
from marshmallow import ValidationError
from api.schedule.model import ScheduleModel, SchedulePOSTSchema, ScheduleGETSchema
from core.db import db


class HelperService():
    # daily registration limit
    dailyLimit = 3

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


class Schedule(Resource, HelperService):
    def get(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        requestDate = request.get_json()

        try:
            # deserializing data structure to an object defined by the Schema's fields
            schema = ScheduleGETSchema()
            schedule = schema.load(requestDate)
        except ValidationError as err:
            return {"err": err.messages}, 400

        # processing to get schedule
        # querying from db
        results = ScheduleModel.query.filter_by(date=schedule.date)

        # serializing object to native Python data types according to the Schema's fields
        schema = ScheduleGETSchema(many=True)
        schedules = schema.dump(results)

        return jsonify({
            "msg": "success",
            "date": schedule.date,
            "schedules": schedules
        })

    def post(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        requestData = request.get_json()

        try:
            # deserializing data structure to an object defined by the Schema's fields
            schema = SchedulePOSTSchema()
            schedule = schema.load(requestData)
        except ValidationError as err:
            return {"err": err.messages}, 400

        # processing to add a schedule
        # already registered??
        if self.alreadyRegistered(schedule.nid):
            return {"err": "this nid already registered"}, 400

        # taking care of date
        if schedule.date:
            if not self.hasSlot(schedule.center, schedule.date, self.dailyLimit):
                freeSlot = self.getNextAvailableSlot(
                    schedule.center, self.dailyLimit)
                return {"err": "no available slot on " + str(schedule.date) + ", next available free slot on " + str(freeSlot)}, 400
        else:
            schedule.date = self.getNextAvailableSlot(
                schedule.center, self.dailyLimit)

        db.session.add(schedule)
        db.session.commit()

        # serializing object to native Python data types according to the Schema's fields
        addedSchedule = schema.dump(schedule)

        return jsonify({
            "msg": "registration successful",
            "schedule": addedSchedule
        })
