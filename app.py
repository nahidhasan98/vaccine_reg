from flask import Flask, jsonify
import mongoengine
from service.registration import vaccineReg


# db connention
def dbConnect():
    host = "mongodb://localhost"
    port = 27017
    alias = "dbSession"
    dbName = "py_flask"

    mongoengine.register_connection(
        alias=alias, db=dbName, host=host, port=port)


# init app
app = Flask('__name__')


# creating route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"msg": "Hello world!"})


@app.route('/reg', methods=['POST'])
def registration():
    vaccineReg()

    return jsonify({"msg": "Hello world!"})


# run server
if __name__ == '__main__':
    dbConnect()

    app.run(debug=True, port=9001)
