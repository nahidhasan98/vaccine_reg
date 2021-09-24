from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from api.user.model import UserModel
from api.login.model import LoginSchema
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

    # logging out the logged in user
    def clearLogIn(self):
        user = getCurrentUser()

        if user:
            user.authenticated = False
            db.session.commit()


class Login(Resource, HelperService):
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

        # already logged in?
        if user.authenticated:
            return {"err": "user already logged in"}, 400

        # password matching
        if login.password != user.password:
            return {"err": "invalid password"}, 401

        # before log in log out other user (if any user logged in already)
        self.clearLogIn()

        # password matched. update logged info to DB
        user.authenticated = True
        db.session.commit()

        return jsonify({
            "msg": "login successful",
            "user": login.email
        })


class Logout(Resource):
    def get(self):
        currentUser = getCurrentUser()

        if not currentUser:
            return {"err": "you are not logged in"}, 400

        currentUser.authenticated = False

        # update DB with logout info
        db.session.commit()

        return jsonify({
            "msg": "logout successful"
        })
