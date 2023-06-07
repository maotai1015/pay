import sqlalchemy as sa

from app.app import db

from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    id = db.Column(sa.Integer, primary_key=True)
    username = db.Column(sa.String(64), comment="姓名")
    phone = db.Column(sa.String(64), comment="手机号")
    password = db.Column(sa.String(64), comment="名称")

    __tablename__ = "user"

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
