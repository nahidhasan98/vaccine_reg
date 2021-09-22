from marshmallow import Schema, fields, post_load
from core.db import db


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


class ScheduleSchema(Schema):
    id = fields.Integer(dump_only=True)
    nid = fields.String()
    center = fields.String()
    date = fields.Date()
    doseCompleted = fields.Integer()

    @post_load
    def create_schedule(self, data, **kwargs):
        return ScheduleModel(**data)
