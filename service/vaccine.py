from flask import request, jsonify, Blueprint
from service.schedule import ScheduleService

blueprint = Blueprint('vaccine', __name__, url_prefix="/vaccine")


# creating route
@blueprint.route('/schedule', methods=['GET'])
def schedule():
    if not request.is_json:
        return jsonify({"err": "no json object provided"}), 400

    date = request.json.get('date')

    # creating object for GetSchedule class
    object = ScheduleService()
    result, err = object.getSchedule(date)

    if err != None:
        return jsonify({"err": err}), 400

    return jsonify({
        "date": date,
        "schedule": result
    })


@blueprint.route('/schedule', methods=['POST'])
def registration():
    if not request.is_json:
        return jsonify({"err": "no json object provided"}), 400

    nid = request.json.get('nid')
    if not nid:
        return jsonify({"err": "nid not provided"}), 400

    center = request.json.get('center')
    if not center:
        return jsonify({"err": "center not provided"}), 400

    date = request.json.get('date')

    # creating object for Registration class
    object = ScheduleService()
    result, err = object.addSchedule(nid, center, date)

    if err != None:
        return jsonify({"err": err}), 400

    return jsonify({
        "msg": "registration successful",
        "vaccination_date": result['date'],
        "vaccination_center": result['center']
    })
