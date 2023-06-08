from flask_restful import Resource, fields, marshal_with, reqparse

from models.supplies import Supplies
from models.user import User

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
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            return {'message': 'Logged in as {}'.format(current_user.username)}
        else:
            return {'message': 'Wrong credentials'}


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        # 查找用户名
        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        # 新建用户
        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password'])
        )
        # 保存数据
        new_user.save_to_db()
        return {
            'message': 'User {} was created'.format(data['username'])
        }