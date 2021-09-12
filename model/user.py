import mongoengine


class User(mongoengine.Document):
    _id = mongoengine.StringField(Required=True)
    firstName = mongoengine.StringField(Required=True)
    lastName = mongoengine.StringField(Required=True)
    nid = mongoengine.StringField(Required=True)

    meta = {
        'db_alias': 'dbSession',
        'collection': 'user'
    }
