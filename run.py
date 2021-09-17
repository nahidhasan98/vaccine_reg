from flask import Flask
from flask_restful import Api
from db import dbConnect, runSeeder
from api.schedule.route import initScheduleRoutes

# init flask app
app = Flask(__name__)
api = Api(app)

# run server
if __name__ == '__main__':
    dbConnect()
    runSeeder(100)
    initScheduleRoutes(api)

    app.run(port=9001, debug=True, use_reloader=False)
