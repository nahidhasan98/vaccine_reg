from marshmallow import Schema, fields, post_load
from api.user import UserModel


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    authenticated = fields.Boolean()

    @post_load
    def create_login(self, data, **kwargs):
        return UserModel(**data)
