from core.db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100))

    def __init__(self, nid, name):
        self.nid = nid
        self.name = name

    # def __repr__(self):
    #     return f"<User {self.name}>"
