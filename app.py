from flask import Flask
# from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config.config import config

# flask初始化
app = Flask(__name__)
app.config.from_object(config)


# 数据库初始化
db = SQLAlchemy()
db.init_app(app)

# 健康检查
app.add_url_rule('/hs', view_func=lambda: "ok")
# def ok():
#     return "ok"
# app.add_url_rule('/hs', view_func=ok)
# ma = Marshmallow()
