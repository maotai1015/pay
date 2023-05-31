from sqlalchemy.orm import Mapped
import sqlalchemy as sa
from typing import List
from typing import Optional
from sqlalchemy.orm import relationship

from app import db


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(sa.Integer, primary_key=True)
    name = db.Column(sa.String(64), comment="名称")
    gender = db.Column(sa.String(64), comment="性别")
