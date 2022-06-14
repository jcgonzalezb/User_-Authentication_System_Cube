from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.role import *
from models.permission import *


# table rolePermission

rolePermission = db.Table('rolePermission',
    db.Column('roleId', db.String(60), db.ForeignKey('role.roleId'), primary_key=True),
    db.Column('permissionId', db.String(60), db.ForeignKey('permission.permissionId'), primary_key=True)
)
