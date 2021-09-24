from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from api.user.model import UserModel
from api.login.model import LoginSchema
from api.jwt.jwt import JWT
from core.db import db
from core.util import getCurrentUser


class HelperService():
    # checking if provided nid is already registered or not
    def isRegisteredEmail(self, email):
        exist = UserModel.query.filter_by(email=email).first()

        if exist:
            return True

        return False

    # checking if provided nid is already registered or not
    def getUserFromDB(self, email):
        user = UserModel.query.filter_by(email=email).first()

        return user


class Login(Resource, HelperService, JWT):
    def post(self):
        if not request.is_json:
            return {"err": "no json object provided"}, 400

        requestData = request.get_json()

        try:
            # deserializing data structure to an object defined by the Schema's fields
            schema = LoginSchema()
            login = schema.load(requestData)
        except ValidationError as err:
            return {"err": err.messages}, 400

        # processing to login
        # registered email?
        if not self.isRegisteredEmail(login.email):
            return {"err": "invalid email. no account found with this email"}, 400

        user = self.getUserFromDB(login.email)

        # password matching
        if login.password != user.password:
            return {"err": "invalid password"}, 402

        # password matched
        # generate jwt token
        token = self.encode_auth_token(login.email)
        token = token.decode("utf-8")

        return jsonify({
            "msg": "login successful",
            "token": token
        })
