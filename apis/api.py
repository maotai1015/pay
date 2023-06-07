from flask_restful import Resource, fields, marshal_with, reqparse

from models.supplies import Supplies

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class GetSupplies(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'describe': fields.String,
        'price': fields.Price,
        'nums': fields.Integer,
        'sum': fields.Price,

    }

    # 装饰器，定义返回数据
    @marshal_with(resource_fields)
    def get(self):
        supplies_list = Supplies.query.all()
        return supplies_list


class Login(Resource):
    def post(self):
        data = parser.parse_args()
        return data


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        return data