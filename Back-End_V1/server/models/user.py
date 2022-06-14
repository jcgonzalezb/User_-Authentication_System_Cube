from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.role import *
from models.user_role import userRole


# table user
class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.String(128), primary_key=True, autoincrement=False)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    cityOfResidence = db.Column(db.String(128))
    countryOfResidence = db.Column(db.String(128))
    photoUrl = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    emailAddress = db.Column(db.String(128))
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=userRole, lazy='subquery',
        back_populates="users")
    startups = db.relationship('Startup', backref='user_id', lazy=True)

    def __init__(self, userId, firstname, lastname, cityOfResidence,
                 countryOfResidence, photoUrl, phone, emailAddress, password, admin):
        self.userId = userId
        self.firstname = firstname
        self.lastname = lastname
        self.cityOfResidence = cityOfResidence
        self.countryOfResidence = countryOfResidence
        self.photoUrl = photoUrl
        self.phone = phone
        self.emailAddress = emailAddress
        self.password = password
        self.admin = admin

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
