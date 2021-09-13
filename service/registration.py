from app import registration
from datetime import datetime, timedelta
import uuid
from model.schedule import Schedule
from model.user import User


# daile registration limit
dailyLimit = 3


# getting next available free slot/date for registration for a specific center
def getNextAvailableSlot(center):
    today = datetime.today()

    rows = Schedule.objects.aggregate([
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
def hasSlot(center, ISODate):
    counter = Schedule.objects(center=center, date=ISODate)

    if len(counter) < dailyLimit:
        return True

    return False


# converting input date to usable format. if invalid, return error message
def getISODate(date):
    try:
        ISODate = datetime.strptime(date, '%d-%m-%y')
    except:
        return False

    if ISODate <= datetime.today():
        return True

    return ISODate


# checking if provided nid is already registered or not
def alreadyRegistered(nid):
    exist = Schedule.objects(nid=nid).first()

    if exist:
        return True

    return False


# checking if provided nid is valid or not
def validNID(nid):
    res = User.objects(nid=nid).first()

    if res:
        return True

    return False


# function for registration
def vaccineReg(nid, center, date):
    s = Schedule()

    s._id = uuid.uuid4().hex
    s.nid = nid
    s.center = center
    s.date = date

    # checking nid validitidy
    if not validNID(nid):
        return "invalid nid"

    # already registered??
    if alreadyRegistered(nid):
        return "this nid already registered"

    # taking care of date
    if date:
        ISODate = getISODate(date)

        if ISODate == False:
            return "invalid date format. required format is: 31-12-21"
        elif ISODate == True:
            return "invalid date. date must be later from today"

        if not hasSlot(center, ISODate):
            freeSlot = getNextAvailableSlot(center)
            return "no available slot on " + date + ", next available free slot on " + str(freeSlot)
        else:
            s.date = ISODate
    else:
        s.date = getNextAvailableSlot(center)

    s.save()
    return s
