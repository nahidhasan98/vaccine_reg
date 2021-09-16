import mongoengine
from config import DB


# db connention
def dbConnect():
    mongoengine.connect(db=DB.dbName, alias=DB.alias,
                        host=DB.host, port=DB.port)
