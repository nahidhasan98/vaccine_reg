from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime, timedelta
from api.user.model import UserModel
from api.schedule.model import ScheduleModel
from extention import db
from sqlalchemy import func


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
        res = UserModel.query.filter_by(nid=nid).first()

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
        today = datetime.today().date()
        print(today, type(today))

        rows = db.session.query(ScheduleModel.date, func.count(ScheduleModel.date).label('count')) \
            .group_by(ScheduleModel.date) \
            .filter(ScheduleModel.center == center, ScheduleModel.date > today) \
            .order_by(ScheduleModel.date.asc())

        # converting CommandCursor object to list
        for row in rows:
            print(row.date, row.count, rows.count())

        # safely assuming slot
        if rows.count() > 0:
            # last registered day + 1
            gotSlot = rows[rows.count()-1].date+timedelta(days=1)
        else:
            # if no registration done in this center
            gotSlot = today+timedelta(days=1)

        # checking if any slot available between total registartion date range
        for row in rows:
            if row.count < dailyLimit:
                gotSlot = row.date
                break

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


class ScheduleService(ValidatorService, HelperService):
    # daily registration limit
    __dailyLimit = 3

    # function for registration
    def addSchedule(self, nid, center, date):
        s = ScheduleModel(
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

        db.session.add(s)
        db.session.commit()
        return s, None

    # function for getting schedule on a specific date
    def getSchedule(self, date):
        # taking care of date
        if not self.validDateInputFormat(date):
            return None, "invalid date format. required format is: 31-12-21"

        ISOFromattedDate = self.getISODateFromString(date)

        # querying from db
        rows = ScheduleModel.query.filter_by(date=ISOFromattedDate)

        # processing to dict for json
        results = []
        for row in rows:
            temp = {
                'id': row.id,
                'nid': row.nid,
                'center': row.center,
                'date': row.date,
                'status': row.status,
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
            "vaccination_date": result.date,
            "vaccination_center": result.center
        })
