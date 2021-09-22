from datetime import datetime
from marshmallow import Schema, fields, post_load
from marshmallow.exceptions import ValidationError
from core.db import db
from api.user import UserModel


class ScheduleModel(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.String(10), unique=True)
    center = db.Column(db.String(200))
    date = db.Column(db.Date)
    doseCompleted = db.Column(db.Integer, default=0)

    def __init__(self, nid, center, date=None):
        self.nid = nid
        self.center = center
        self.date = date

    def __repr__(self):
        return f'ScheduleModel ("id": {self.id}, "nid": {self.nid}, "center": {self.center}, "date": {self.date}, "doseCompleted": {self.doseCompleted})'


class CustomValidator():
    # checking if provided date is later from today or not
    def previousDate(date):
        if date <= datetime.today().date():
            raise ValidationError(
                'invalid date. date must be later from today')

    # checking if provided nid is valid or not
    def validNID(nid):
        res = UserModel.query.filter_by(nid=nid).first()

        if not res:
            raise ValidationError('invalid nid')


class ScheduleSchema(Schema):
    id = fields.Integer(dump_only=True)
    nid = fields.String(required=True, validate=CustomValidator.validNID)
    center = fields.String(required=True)
    date = fields.Date(validate=CustomValidator.previousDate)
    doseCompleted = fields.Integer()

    @post_load
    def create_schedule(self, data, **kwargs):
        return ScheduleModel(**data)
