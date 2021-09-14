from datetime import datetime, timedelta
import uuid
from model.schedule import Schedule
from model.user import User


class ISODate:
    date = None

    # constructor
    def __init__(self, date):
        self.date = date

    def _validInputFormat(self):
        try:
            ISOFromattedDate = datetime.strptime(self.date, '%d-%m-%y')
        except:
            return False

        return ISOFromattedDate

    # converting input date to usable format. if invalid, return error message

    def _getISODate(self):
        ISOFromattedDate = self._validInputFormat()

        if not ISOFromattedDate:
            return False

        if ISOFromattedDate <= datetime.today():
            return True

        return ISOFromattedDate


class Registration(ISODate):
    # daily registration limit
    dailyLimit = 3

    # constructor
    def __init__(self, nid, center, date):
        self.nid = nid
        self.center = center
        self.date = date
        ISODate.__init__(self, date)

    # getting next available free slot/date for registration for a specific center

    def __getNextAvailableSlot(self):
        today = datetime.today()

        rows = Schedule.objects.aggregate([
            {
                '$match': {'center': self.center, 'date': {'$gt': today}}
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
            if row['totalCount'] < self.dailyLimit:
                gotSlot = row['_id']
                break

        return gotSlot

    # checking available free slot for registration for a specific center and date

    def __hasSlot(self, ISODate):
        counter = Schedule.objects(center=self.center, date=ISODate)

        if len(counter) < self.dailyLimit:
            return True

        return False

    # checking if provided nid is already registered or not

    def __alreadyRegistered(self):
        exist = Schedule.objects(nid=self.nid).first()

        if exist:
            return True

        return False

    # checking if provided nid is valid or not

    def __validNID(self):
        res = User.objects(nid=self.nid).first()

        if res:
            return True

        return False

    # function for registration

    def _vaccineRegistration(self):
        s = Schedule()

        s._id = uuid.uuid4().hex
        s.nid = self.nid
        s.center = self.center
        s.date = self.date

        # checking nid validitidy
        if not self.__validNID():
            return "invalid nid"

        # already registered??
        if self.__alreadyRegistered():
            return "this nid already registered"

        # taking care of date
        if self.date:
            ISODate = self._getISODate()

            if ISODate == False:
                return "invalid date format. required format is: 31-12-21"
            elif ISODate == True:
                return "invalid date. date must be later from today"

            if not self.__hasSlot(ISODate):
                freeSlot = self.__getNextAvailableSlot()
                return "no available slot on " + self.date + ", next available free slot on " + str(freeSlot)
            else:
                s.date = ISODate
        else:
            s.date = self.__getNextAvailableSlot()

        s.save()
        return s


class GetSchedule(ISODate):
    # constructor
    def __init__(self, date):
        ISODate.__init__(self, date)

    # function for getting schedule on a specific date

    def _getSchedule(self):
        # taking care of date
        ISODate = self._validInputFormat()

        if not ISODate:
            return "invalid date format. required format is: 31-12-21"

        # querying from db
        rows = Schedule.objects(date=ISODate)

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

        return results
