from flask import Flask
from config import DB
from api.schedule import Schedule_BP
from core.db import db
from core.util import seedUserFromJSON


# init flask app
app = Flask(__name__)

# setting up app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + \
    DB.dbUser+":"+DB.dbPass+"@"+DB.host+":"+DB.port+"/"+DB.dbName
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# innitializing db
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()
    # loading user data from faker generator
    # seedUserFromFakerGenerator(100)

    # loading user data from json file
    seedUserFromJSON()


# registering blueprint with flask app
app.register_blueprint(Schedule_BP)

# run server
if __name__ == '__main__':
    app.run(port=9001, debug=True, use_reloader=False)
