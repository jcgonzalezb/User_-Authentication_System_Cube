from flask_marshmallow import Marshmallow
from schemas.ma import ma


class IndustrySchema(ma.Schema):
    class Meta:
        fields = ("industryId", "industryName")
