from flask_sqlalchemy import SQLAlchemy
from models.db import db
from models.user import User
from models.kpiRegister import *


# table startup
class Startup(db.Model):
    __tablename__ = 'startup'

    startupId = db.Column(db.String(60), primary_key=True)
    userId = db.Column(db.String(60), db.ForeignKey('user.userId'))
    name = db.Column(db.String(128))
    photoUrl = db.Column(db.String(128))
    country = db.Column(db.String(60))
    city = db.Column(db.String(60))
    emailAddress = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    femaleFounders = db.Column(db.Integer)
    founders = db.Column(db.Integer)
    industry = db.Column(db.String(60), db.ForeignKey('industry.industryId'))
    active = db.Column(db.Boolean)
    registers = db.relationship('KpiRegister', backref='startup_id', lazy=True)

    def __init__(self, startupId, userId, name, photoUrl, country, city,
                 emailAddress, phone, founders, femaleFounders, industry,
                 active):
        self.startupId = startupId
        self.userId = userId
        self.name = name
        self.photoUrl = photoUrl
        self.country = country
        self.city = city
        self.emailAddress = emailAddress
        self.phone = phone
        self.founders = founders
        self.femaleFounders = femaleFounders
        self.industry = industry
        self.active = active
