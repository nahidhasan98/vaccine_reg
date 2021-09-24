import os
from flask import json
from flask_seeder import Faker, generator
from api.user.model import UserModel
from marshmallow import ValidationError
from api.user.model import UserSchema
from core.db import db


def seedUserFromFakerGenerator(limit):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
        cls=UserModel,
        init={
            "nid": generator.String('[1-9][0-9]{9}'),
            "name": generator.Name(),
            "email": generator.Email(),
            "password": generator.String('[a-z]{8}')
        },
    )
    # deleting old data
    # user = User
    # user.drop_collection()

    # Create 100 users
    for user in faker.create(limit):
        db.session.add(user)
        db.session.commit()


def seedUserFromJSON():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static/data", "user.json")
    userData = json.load(open(json_url))

    try:
        # deserializing data structure to an object defined by the Schema's fields
        schema = UserSchema(many=True)
        user = schema.load(userData)
    except ValidationError as err:
        print(err)

    try:
        db.session.add_all(user)
        db.session.commit()
    except:
        print("Data alredy loaded in DB")
