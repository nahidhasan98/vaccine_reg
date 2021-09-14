import mongoengine


# db connention
def dbConnect():
    host = "mongodb://localhost"
    port = 27017
    alias = "dbSession"
    dbName = "py_flask"

    mongoengine.connect(db=dbName, alias=alias, host=host, port=port)
