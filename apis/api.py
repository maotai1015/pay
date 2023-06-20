import csv
import json
from io import StringIO

from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.supplies import Supplies, Record
from models.user import User
from flask import Response
from flask import stream_with_context

class SuppliesOpt(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'describe': fields.String,
        'price': fields.Price,
        'nums': fields.Integer,
        'sum': fields.Price,

    }

    # 定义返回数据
    @marshal_with(resource_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        data = parser.parse_args()
        name = data.get("name", "")

        dbclone = Supplies.query
        if name:
            dbclone = dbclone.filter(Supplies.name.like(f"%{name}%"))
        supplies_list = dbclone.all()
        return supplies_list

    @jwt_required(refresh=True)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='This field cannot be blank', required=True)
        parser.add_argument('describe')
        parser.add_argument('price', type=float, help='This field cannot be blank', required=True)
        parser.add_argument('nums', type=float, help='This field cannot be blank', required=True)

        data = parser.parse_args()
        is_supply = Supplies.find_by_name(data["name"])
        if is_supply:
            return {
                "code": 1,
                "message": "失败!已存在该物品"
            }

        new_supply = Supplies(
            name=data["name"],
            describe=data["describe"],
            price=data["price"],
            nums=data["nums"],
            sum=data["price"]*data["nums"]
        )
        new_supply.save_to_db()
        return {
            "code": 0,
            "message": "添加成功"
        }

    @jwt_required(refresh=True)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='This field cannot be blank', required=True)
        parser.add_argument('describe')
        parser.add_argument('price', type=float, help='This field cannot be blank', required=True)
        parser.add_argument('nums', type=float, help='This field cannot be blank', required=True)

        data = parser.parse_args()
        is_supply = Supplies.find_by_name(data["name"])
        if not is_supply:
            return {
                "code": 1,
                "message": "失败!不存在该物品"
            }
        is_supply.name = data.get("name", "")

        is_supply.save_to_db()
        return {
            "code": 0,
            "message": "修改成功"
        }

    @jwt_required(refresh=True)
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        is_supply = Supplies.find_by_name(data["name"])
        if not is_supply:
            return {
                "code": 1,
                "message": "失败!不存在该物品"
            }
        is_supply.delete_from_db()
        return {
            "code": 0,
            "message": "删除成功"
        }


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'code': 0,
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                    }
        else:
            return {'message': 'Wrong credentials'}


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        print("123")
        data = parser.parse_args()
        print("456")
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
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {
            'message': 'User {} was created'.format(data['username']),
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class TokenRefresh(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class RecordOpt(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='This field cannot be blank', required=True)
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('opt', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        useropt = User.find_by_username(data['username'])
        supplyopt = Supplies.find_by_name(data['name'])

        if data["opt"] == "back":
            res = Record.query.filter(Record.sup_id == supplyopt.id, Record.user_id == useropt.id).first()
            if not res:
                return {
                    'message': "not record",
                    "code": 1
                }
            res.is_back = 1
            res.save_to_db()
        elif data["opt"] == "out":
            new_record = Record(
                sup_id=supplyopt.id,
                user_id=useropt.id,
                is_back=0
            )
            new_record.save_to_db()
        else:
            return {
                'message': "error operate",
                "code": 1
            }
        return {
            "code": 0,
            "message": "ok"
        }

class DownLoad(Resource):
    def get(self):
        res = []
        data = SuppliesOpt().get()
        res = [data[0].keys()]
        for i in data:
            res.append(i.values())
        def generate():
            #	用 StringIO 在内存中写，不会生成实际文件
            io = StringIO()  # 在 io 中写 csv
            w = csv.writer(io)
            for i in res:  # 对于 data 中的每一条
                w.writerow(i)  # 传入的是一个数组 ['xxx','xxx@xxx.xxx'] csv.writer 会把它处理成逗号分隔的一行
                # 需要注意的是传入仅一个字符串 '' 时，会被逐字符分割，所以要写成 ['xxx'] 的形式
                yield io.getvalue()  # 返回写入的值
                io.seek(0)  # io流的指针回到起点
                io.truncate(0)  # 删去指针之后的部分，即清空所有写入的内容，准备下一行的写入

        response = Response(generate(), mimetype='text/csv')

        response.headers.set("Content-Disposition", "attachment", filename="111.csv")
        return response