from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config.config import config

# flask初始化
app = Flask(__name__)
app.config.from_object(config)


# 数据库初始化
db = SQLAlchemy()
db.init_app(app)

ma = Marshmallow()
