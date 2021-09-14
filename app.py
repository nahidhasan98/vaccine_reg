from flask import Flask, request, jsonify
from service.schedule import Registration, GetSchedule
from db.connection import dbConnect
from db.seeder import runSeeder
from model.schedule import Schedule


# init flask app
app = Flask('__name__')


# creating route
@app.route('/', methods=['GET'])
def schedule():
    if not request.is_json:
        return jsonify({"msg": "no json object provided"}), 400

    date = request.json.get('date')

    status = GetSchedule(date)
    status = status._getSchedule()

    if type(status) != Schedule:
        return jsonify({"msg": status})

    return jsonify({
        "date": status['date'],
        "schedule": status
    })


@app.route('/reg', methods=['POST'])
def registration():
    if not request.is_json:
        return jsonify({"msg": "no json object provided"}), 400

    nid = request.json.get('nid')
    if not nid:
        return jsonify({"msg": "nid not provided"}), 400

    center = request.json.get('center')
    if not center:
        return jsonify({"msg": "center not provided"}), 400

    date = request.json.get('date')

    status = Registration(nid, center, date)
    status = status._vaccineRegistration()

    if type(status) != Schedule:
        return jsonify({"msg": status})

    return jsonify({
        "msg": "registration successful",
        "vaccination_date": status['date'],
        "vaccination_center": status['center']
    })


# run server
if __name__ == '__main__':
    dbConnect()
    runSeeder(100)

    app.run(port=9001, debug=True, use_reloader=False)
