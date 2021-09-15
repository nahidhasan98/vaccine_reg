import uuid
from model.schedule import ScheduleModel
from service.validator import ValidatorService
from service.helper import HelperService


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
