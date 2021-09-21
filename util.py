from flask_seeder import Faker, generator
from api.user.model import UserModel
from extention import db


def runSeeder(limit):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
        cls=UserModel,
        init={
            "name": generator.Name(),
            "nid": generator.String('[1-9][0-9]{9}')
        },
    )
    # deleting old data
    # user = User
    # user.drop_collection()

    # Create 100 users
    for user in faker.create(limit):
        db.session.add(user)
        db.session.commit()
