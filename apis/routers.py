from flask import Blueprint
from flask_restful import Api

from apis.api import GetAll

api_bp = Blueprint('api', __name__, url_prefix='/api')
api_restful = Api(api_bp)
# 健康检查

api_restful.add_resource(GetAll, '/all')


