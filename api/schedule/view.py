from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime, timedelta
import uuid

from werkzeug.sansio.multipart import State
from api.user.model import UserModel
from .model import ScheduleModel


class ValidatorService():
    # checking if provided date format is valid or not
    def validDateInputFormat(self, date):
        try:
            _ = datetime.strptime(date, '%d-%m-%y')
        except:
            return False

        return True

    # checking if provided date is later from today or not
    def validDate(self, date):
        ISODate = datetime.strptime(date, '%d-%m-%y')

        if ISODate <= datetime.today():
            return False

        return True

    # checking if provided nid is valid or not
    def validNID(self, nid):
        res = UserModel.objects(nid=nid).first()

        if res:
            return True

        return False


class HelperService():
    # converting input date(type string) to usable format(type date)
    def getISODateFromString(self, date):
        ISOFromattedDate = datetime.strptime(date, '%d-%m-%y')

        return ISOFromattedDate

    # getting next available free slot/date for registration for a specific center
    def getNextAvailableSlot(self, center, dailyLimit):
        today = datetime.today()

        rows = ScheduleModel.objects.aggregate([
            {
                '$match': {'center': center, 'date': {'$gt': today}}
            },
            {
                '$group': {'_id': '$date', 'totalCount': {'$sum': 1}}
            },
            {
                '$sort': {'_id': 1}
            }
        ])

        # converting CommandCursor object to list
        rows = list(rows)

        # safely assuming slot
        if len(rows) > 0:
            # last registered day + 1
            gotSlot = rows[len(rows)-1]['_id']+timedelta(days=1)
        else:
            # if no registration done in this center
            gotSlot = today+timedelta(days=1)

        # checking if any slot available between total registartion date range
        for row in rows:
            if row['totalCount'] < dailyLimit:
                gotSlot = row['_id']
                break

        return gotSlot

    # checking available free slot for registration for a specific center and date
    def hasSlot(self, center, date, dailyLimit):
        counter = ScheduleModel.objects(center=center, date=date)

        if len(counter) < dailyLimit:
            return True

        return False

    # checking if provided nid is already registered or not
    def alreadyRegistered(self, nid):
        exist = ScheduleModel.objects(nid=nid).first()

        if exist:
            return True

        return False


class ScheduleService(ValidatorService, HelperService):
    # daily registration limit
    __dailyLimit = 3

    # function for registration
    def addSchedule(self, nid, center, date):
        s = ScheduleModel(
            _id=uuid.uuid4().hex,
            nid=nid,
            center=center,
            date=date
        )

        # checking nid validitidy
        if not self.validNID(nid):
            return None, "invalid nid"

        # already registered??
        if self.alreadyRegistered(nid):
            return None, "this nid already registered"

        # taking care of date
        if date:
            if not self.validDateInputFormat(date):
                return None, "invalid date format. required format is: 31-12-21"

            if not self.validDate(date):
                return None, "invalid date. date must be later from today"

            ISOFromattedDate = self.getISODateFromString(date)

            if not self.hasSlot(center, ISOFromattedDate, self.__dailyLimit):
                freeSlot = self.getNextAvailableSlot(center, self.__dailyLimit)
                return None, "no available slot on " + date + ", next available free slot on " + str(freeSlot)
            else:
                s.date = ISOFromattedDate
        else:
            s.date = self.getNextAvailableSlot(center, self.__dailyLimit)

        s.save()
        return s, None

    # function for getting schedule on a specific date
    def getSchedule(self, date):
        # taking care of date
        if not self.validDateInputFormat(date):
            return None, "invalid date format. required format is: 31-12-21"

        ISOFromattedDate = self.getISODateFromString(date)

        # querying from db
        rows = ScheduleModel.objects(date=ISOFromattedDate)

        # processing to dict for json
        results = []
        for row in rows:
            temp = {
                '_id': row['_id'],
                'nid': row['nid'],
                'center': row['center'],
                'date': row['date'],
                'status': row['status'],
            }
            results.append(temp)

        return results, None


class Schedule(Resource):
    def get(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        date = request.json.get('date')

        # creating object for GetSchedule class
        object = ScheduleService()
        result, err = object.getSchedule(date)

        if err != None:
            return {"err": err}, 400

        return jsonify({
            "date": date,
            "schedule": result
        })

    def post(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        nid = request.json.get('nid')
        if not nid:
            return {"err": "nid not provided"}, 400

        center = request.json.get('center')
        if not center:
            return {"err": "center not provided"}, 400

        date = request.json.get('date')

        # creating object for Registration class
        object = ScheduleService()
        result, err = object.addSchedule(nid, center, date)

        if err != None:
            return {"err": err}, 400

        return jsonify({
            "msg": "registration successful",
            "vaccination_date": result['date'],
            "vaccination_center": result['center']
        })
