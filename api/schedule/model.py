from extention import db


class ScheduleModel(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.String(10), unique=True)
    center = db.Column(db.String(200))
    date = db.Column(db.Date)
    status = db.Column(db.Boolean)

    def __init__(self, nid, center, date):
        self.nid = nid
        self.center = center
        self.date = date
        self.status = False

    # def __repr__(self):
    #     return f"<Schedule {self.nid}>"
