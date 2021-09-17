import mongoengine


class ScheduleModel(mongoengine.Document):
    _id = mongoengine.StringField(required=True)
    nid = mongoengine.StringField(required=True)
    center = mongoengine.StringField(required=True)
    date = mongoengine.DateField(required=True)
    status = mongoengine.BooleanField(required=True, default=False)

    meta = {
        'db_alias': 'dbSession',
        'collection': 'schedule'
    }
