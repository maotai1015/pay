from app import db
import sqlalchemy as sa


class Supplies(db.Model):
    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(64), comment="名称")
    describe = db.Column(sa.String(64), comment="描述")
    price = db.Column(sa.DECIMAL, comment="单价")
    nums = db.Column(sa.Integer, comment="数量")
    sum = db.Column(sa.DECIMAL, comment="总价")

    __tablename__ = "asset_supplies"


def get_all():
    pass


