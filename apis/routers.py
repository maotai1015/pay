from apis.api import GetSupplies, UserRegistration, Login
from app.app import api_restful

api_restful.add_resource(GetSupplies, '/supply')
api_restful.add_resource(UserRegistration, '/register')
api_restful.add_resource(Login, '/login')


