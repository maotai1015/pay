import sqlalchemy as sa

from app.app import db

from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    id = db.Column(sa.Integer, primary_key=True)
    username = db.Column(sa.String(64), comment="用户名", unique=True)
    phone = db.Column(sa.String(64), comment="手机号")
    password = db.Column(sa.String(256), comment="密码")

    __tablename__ = "user"

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
