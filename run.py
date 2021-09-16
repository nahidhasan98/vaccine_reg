from service import app
from db import dbConnect, runSeeder

# run server
if __name__ == '__main__':
    dbConnect()
    runSeeder(100)

    app.run(port=9001, debug=True, use_reloader=False)
