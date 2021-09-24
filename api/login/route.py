from flask import Blueprint
from flask_restful import Api
from api.login.view import Login

# creating blueprint
Login_BP = Blueprint('Login_BP', __name__, url_prefix='/api')

# passing blueprint to restful.Api. Later this will add route
api = Api(Login_BP)

# creating route
api.add_resource(Login, '/login')
