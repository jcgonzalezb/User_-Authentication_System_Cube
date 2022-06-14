from flask_marshmallow import Marshmallow
from schemas.ma import ma


class StartupSchema(ma.Schema):
    class Meta:
        fields = ('startupId', 'userId','name', 'photoUrl', 'country', 'city',
                  'emailAddress', 'phone', 'founders', 'femaleFounders',
                  'industry', 'active')
