from flask import Flask
from db import dbConnect, runSeeder
from api.schedule.route import Schedule_BP

# init flask app
app = Flask(__name__)

# registering blueprint with flask app
app.register_blueprint(Schedule_BP)

# run server
if __name__ == '__main__':
    dbConnect()
    runSeeder(100)

    app.run(port=9001, debug=True, use_reloader=False)
