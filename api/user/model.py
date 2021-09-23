from marshmallow import Schema, fields, post_load
from core.db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'UserModel ("id": {self.id}, "nid": {self.nid}, "name": {self.name})'


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    nid = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return UserModel(**data)
