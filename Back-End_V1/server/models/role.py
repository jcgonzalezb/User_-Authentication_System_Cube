from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.permission import *
from models.role_permission import rolePermission
from models.user import *
from models.user_role import userRole


# table role
class Role(db.Model):
    __tablename__ = 'role'

    roleId = db.Column(db.String(60), primary_key=True)
    role = db.Column(db.String(60))
    permissions = db.relationship('Permission', secondary=rolePermission, lazy='subquery',
        back_populates="roles")

    users = db.relationship('User', secondary=userRole, lazy='subquery',
        back_populates="roles")


    def __init__(self, roleId, role):
        self.roleId = roleId
        self.role = role
