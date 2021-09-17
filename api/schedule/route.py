
from .view import Schedule


def initScheduleRoutes(api):
    api.add_resource(Schedule, '/api/schedule')
