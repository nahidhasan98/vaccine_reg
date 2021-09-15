from datetime import datetime
from model.user import UserModel


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
