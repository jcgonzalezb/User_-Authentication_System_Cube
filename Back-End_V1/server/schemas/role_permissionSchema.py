from flask_marshmallow import Marshmallow
from schemas.ma import ma


class Role_permissionSchema(ma.Schema):
    class Meta:
        fields = ("roleId", "permissionId")
