from flask import Flask
from .vaccine import blueprint

# init flask app
app = Flask('__name__')


app.register_blueprint(blueprint)
