from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.role import *
from models.role_permission import rolePermission


# table permission
class Permission(db.Model):
    __tablename__ = 'permission'

    permissionId = db.Column(db.String(60), primary_key=True)
    permissionRight = db.Column(db.String(128))
    roles = db.relationship('Role', secondary=rolePermission, lazy='subquery',
        back_populates="permissions")

    def __init__(self, permissionId, permissionRight):
        self.permissionId = permissionId
        self.permissionRight = permissionRight
