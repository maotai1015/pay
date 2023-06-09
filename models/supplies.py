import sqlalchemy as sa
# 资源记录
from app.app import db


class Supplies(db.Model):
    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(64), comment="名称", unique=True)
    describe = db.Column(sa.String(64), comment="描述")
    price = db.Column(sa.DECIMAL, comment="单价")
    nums = db.Column(sa.Integer, comment="数量")
    sum = db.Column(sa.DECIMAL, comment="总价")

    __tablename__ = "asset_supplies"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

# 借用记录
class Record(db.Model):
    id = db.Column(sa.Integer, primary_key=True)
    sup_id = db.Column(sa.String(64), comment="姓名")
    user_id = db.Column(sa.String(64), comment="手机号")
    is_back = db.Column(sa.Integer, comment="是否归还")

    __tablename__ = "record"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
