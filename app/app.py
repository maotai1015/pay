from flask import Flask
from flask import Blueprint
from flask_restful import Api
from config.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# flask初始化
app = Flask(__name__)
app.config.from_object(config)

# 蓝图初始化
api_bp = Blueprint('api', __name__, url_prefix='/api')
api_restful = Api(api_bp)
app.register_blueprint(api_bp)

# 初始化JWT
app.config["JWT_SECRET_KEY"] = "TongGeNiuBi"
jwt = JWTManager(app)

# 数据库初始化
db = SQLAlchemy()
db.init_app(app)

app.add_url_rule('/hs', view_func=lambda: "ok")

from models import *
with app.app_context():
    db.create_all()
