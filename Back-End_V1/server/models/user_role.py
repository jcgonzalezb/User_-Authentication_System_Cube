from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.user import *
from models.role import *


# table userRole

userRole = db.Table('userRole',
    db.Column('roleId', db.String(60), db.ForeignKey('role.roleId'), primary_key=True),
    db.Column('userId', db.String(60), db.ForeignKey('user.userId'), primary_key=True)
)
