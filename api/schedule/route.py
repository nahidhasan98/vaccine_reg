from flask import Blueprint
from flask_restful import Api
from api.schedule.view import Schedule

# creating blueprint
Schedule_BP = Blueprint('Schedule_BP', __name__, url_prefix='/api')

# passing blueprint to restful.Api. Later this will add route
api = Api(Schedule_BP)

# creating route
api.add_resource(Schedule, '/schedule')
