import mongoengine


# db connention
def dbConnect():
    host = "mongodb://localhost"
    port = 27017
    alias = "dbSession"
    dbName = "py_flask"

    mongoengine.register_connection(
        alias=alias, db=dbName, host=host, port=port)
