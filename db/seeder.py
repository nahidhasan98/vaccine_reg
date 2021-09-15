from flask_seeder import Faker, generator
from model.user import UserModel
from uuid import uuid4


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
        user["_id"] = uuid4().hex
        user.save()
