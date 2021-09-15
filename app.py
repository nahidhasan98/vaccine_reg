from flask import Flask, request, jsonify
from db.connection import dbConnect
from db.seeder import runSeeder
from service.schedule import ScheduleService


# init flask app
app = Flask('__name__')


# creating route
@app.route('/schedule', methods=['GET'])
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


@app.route('/schedule', methods=['POST'])
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


# run server
if __name__ == '__main__':
    dbConnect()
    runSeeder(100)

    app.run(port=9001, debug=True, use_reloader=False)
