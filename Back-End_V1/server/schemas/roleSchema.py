from flask_marshmallow import Marshmallow
from schemas.ma import ma


class RoleSchema(ma.Schema):
    class Meta:
        fields = ("roleId", "role")
