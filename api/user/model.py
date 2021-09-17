import mongoengine


class UserModel(mongoengine.Document):
    _id = mongoengine.StringField(Required=True,)
    name = mongoengine.StringField(Required=True)
    nid = mongoengine.StringField(Required=True)

    meta = {
        'db_alias': 'dbSession',
        'collection': 'user'
    }
