from flask_marshmallow import Marshmallow
from schemas.ma import ma


class KpiRegisterSchema(ma.Schema):
    class Meta:
        fields = ("kpiId", "date", "startupId", "revenue", "ARR", "EBITDA", "GMV",
                 "numberEmployees", "fundRaising", "CAC", "activeClients")
