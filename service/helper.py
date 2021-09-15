from datetime import datetime, timedelta
from model.schedule import ScheduleModel


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
