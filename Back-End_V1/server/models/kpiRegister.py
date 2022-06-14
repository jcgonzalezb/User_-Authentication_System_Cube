from flask_sqlalchemy import SQLAlchemy
from models.db import db

# table kpiRegister
class KpiRegister(db.Model):
    __tablename__ = 'kpiRegister'

    kpiId = db.Column(db.String(60), primary_key=True)
    date = db.Column(db.DateTime)
    startupId = db.Column(db.String(60), db.ForeignKey('startup.startupId'))
    revenue = db.Column(db.Float)
    ARR = db.Column(db.Float)
    EBITDA = db.Column(db.Float)
    GMV = db.Column(db.Float)
    numberEmployees = db.Column(db.Integer)
    fundRaising = db.Column(db.Float)
    CAC = db.Column(db.Float)
    activeClients = db.Column(db.Integer)

    def __init__(self, kpiId, date, startupId, revenue, ARR, EBITDA, GMV,
                 numberEmployees, fundRaising, CAC, activeClients):

        self.kpiId = kpiId
        self.date = date
        self.startupId = startupId
        self.revenue = revenue
        self.ARR = ARR
        self.EBITDA = EBITDA
        self.GMV = GMV
        self.numberEmployees = numberEmployees
        self.fundRaising = fundRaising
        self.CAC = CAC
        self.activeClients = activeClients
