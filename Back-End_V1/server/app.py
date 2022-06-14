from json.tool import main
from crypt import methods
from unicodedata import name
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from flask_marshmallow import Marshmallow
from models.db import app, db
from models.industry import Industry
from models.role import Role
from models.startup import Startup
from models.permission import Permission
from models.user import *
from models.kpiRegister import KpiRegister
from models.user_role import userRole
from schemas.ma import ma
from schemas.industrySchema import IndustrySchema
from schemas.roleSchema import RoleSchema
from schemas.startupSchema import StartupSchema
from schemas.permissionSchema import PermissionSchema
from schemas.userSchema import UserSchema
from schemas.kpiRegisterSchema import KpiRegisterSchema
from schemas.role_permissionSchema import Role_permissionSchema
from schemas.user_roleSchema import User_roleSchema
from sqlalchemy import exc
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app.config['SECRET_KEY'] = 'LMhHnM9~,xUy@A&t'

db.create_all()


# One response
startup_schema = StartupSchema()
user_schema = UserSchema()
kpi_register_schema = KpiRegisterSchema()

# Many responses
startup_schemas = StartupSchema(many=True)
user_schemas = UserSchema(many=True)
kpi_register_schemas = KpiRegisterSchema(many=True)

#Decorator for token support

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256', ])
            current_user = User.query.filter_by(emailAddress=data['emailAddress']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

#Testing user access. No token needed
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})


#Testing user access. Token needed
@app.route('/protected')
@token_required
def protected(current_user):
    return jsonify({'message' : 'This is on available for people with valid tokens.'})


#Login endpoint. No @token_required needed.

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(emailAddress=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'emailAddress' : user.emailAddress, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


# Get all users, startups and KPIs. 

@app.route('/api/v1/<val>', methods=['GET'])
@token_required
def get_registers(current_user, val):
    if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
    if val == "startup":
        table = Startup
        val_schemas = startup_schemas
    elif val == "user":
        table = User
        val_schemas = user_schemas
    elif val == "kpi":
        table = KpiRegister
        val_schemas = kpi_register_schemas
    
    #val_id = exec("%s" % ("table."+val+"Id"))
    results = table.query.all()
    val_results = val_schemas.dump(results)
    return jsonify(val_results)


# Get specific user, startup or KPI using id. 

@app.route('/api/v1/<val>/<id>', methods=['GET'])
@token_required
def get_register_by_id(current_user, val, id):
    if val == "startup":
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
        table = Startup
        val_schema = startup_schema
        val_id = table.startupId
    elif val == "user":
        if not current_user.admin:
            return jsonify({'message' : 'Cannot perform that function!'})
        table = User
        val_schema = user_schema
        val_id = table.userId
    elif val == "kpi":
        table = KpiRegister
        val_schema = kpi_register_schema
        val_id = table.kpiId
    try:
        result = table.query.filter(val_id == id).one()
    except NoResultFound:
        return {"message": "{} could not be found.".format(val)}, 400
    return val_schema.jsonify(result)


# Get startup info from user id. 

@app.route('/api/v1/user_startup/<id>', methods=['GET'])
@token_required
def get_user_pyme(current_user, id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    try:
        user = User.query.filter(User.userId == id).one()
    except NoResultFound:
        return {"message": "User could not be found."}, 400
    result = user_schema.dump(user)  # return a writable json
    startup_result = Startup.query.filter(Startup.userId == result["userId"]).one()
    [result.pop(key) for key in ['userId', 'password']]
    result_dict = startup_schema.dump(startup_result)
    [result_dict.pop(key) for key in ['founders', 'femaleFounders',
                                      'industry', 'userId']]
    result['startup'] = result_dict

    return result


#Create new user

@app.route('/api/v1/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(userId =str(uuid.uuid4()), password=hashed_password, cityOfResidence=data['cityOfResidence'],
                countryOfResidence=data['countryOfResidence'], emailAddress=data['emailAddress'], firstname=data['firstname'],
                lastname=data['lastname'], phone=data['phone'], photoUrl=data['photoUrl'], admin=data['admin'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


#Update user information

@app.route('/api/v1/user/<userId>', methods=['PUT'])
@token_required
def update_user(current_user, userId):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(userId=userId).first()
    #print(user)

    if not user:
        return jsonify({'message' : 'No user found!'})

    data = request.get_json()
    user.password=data['password']
    user.cityOfResidence=data['cityOfResidence']
    user.countryOfResidence=data['countryOfResidence']
    user.emailAddress=data['emailAddress']
    user.firstname=data['firstname']
    user.lastname=data['lastname']
    user.phone=data['phone']
    user.photoUrl=data['photoUrl']
    user.admin=data['admin']
    #print(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been updated!'})

#Delete user
@app.route('/api/v1/user/<userId>', methods=['DELETE'])
@token_required
def delete_user(current_user, userId):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(userId=userId).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})


#Create new startup

@app.route('/api/v1/startup', methods=['POST'])

def create_startup():
  
    data = request.get_json()

    new_startup = Startup(startupId = data['startupId'], userId=data['userId'], name=data['name'],
        photoUrl=data['photoUrl'], country=data['country'], city=data['city'],
        emailAddress=data['emailAddress'], phone=data['phone'], founders=data['founders'],
        femaleFounders=data['femaleFounders'], industry=data['industry'], active=data['active'])
    db.session.add(new_startup)
    db.session.commit()

    return jsonify({'message' : 'New startup created!'})

#Update startup information

@app.route('/api/v1/startup/<startupId>', methods=['PUT'])
@token_required
def update_startup(current_user, startupId):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    startup = Startup.query.filter_by(startupId=startupId).first()
    #print(startup)

    if not startup:
        return jsonify({'message' : 'No startup found!'})

    data = request.get_json()
    startup.userId=data['userId']
    startup.name=data['name']
    startup.photoUrl=data['photoUrl']
    startup.country=data['country']
    startup.city=data['city']
    startup.emailAddress=data['emailAddress']
    startup.phone=data['phone']
    startup.founders=data['founders']
    startup.femaleFounders=data['femaleFounders']
    startup.industry=data['industry']
    startup.active=data['active']
    #print(startup)
    db.session.commit()

    return jsonify({'message' : 'The startup has been updated!'})


#Delete startup
@app.route('/api/v1/startup/<startupId>', methods=['DELETE'])
@token_required
def delete_startup(current_user, startupId):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    startup = Startup.query.filter_by(startupId=startupId).first()

    if not startup:
        return jsonify({'message' : 'No startup found!'})

    db.session.delete(startup)
    db.session.commit()

    return jsonify({'message' : 'The startup has been deleted!'})



#create new kpi register

@app.route('/api/v1/kpi', methods=['POST'])
@token_required
def kpi_register(current_user):

    data = request.get_json()

    new_kpi = KpiRegister(kpiId = data['kpiId'], date=data['date'], startupId=data['startupId'],
        revenue=data['revenue'], ARR=data['ARR'], EBITDA=data['EBITDA'], GMV=data['GMV'],
        numberEmployees=data['numberEmployees'], fundRaising=data['fundRaising'], CAC=data['CAC'],
        activeClients=data['activeClients'])
    db.session.add(new_kpi)
    db.session.commit()

    return jsonify({'message' : 'New kpi register created!'})


#Update kpi register

@app.route('/api/v1/kpi/<kpiId>', methods=['PUT'])
@token_required
def update__kpi_register(current_user, kpiId):

    kpiregister = KpiRegister.query.filter_by(kpiId=kpiId).first()
    #print(kpiregister)

    if not kpiregister:
        return jsonify({'message' : 'No kpi register found!'})

    data = request.get_json()
    #print(data)
    kpiregister.date=data['date']
    kpiregister.startupId=data['startupId']
    kpiregister.revenue=data['revenue']
    kpiregister.ARR=data['ARR']
    kpiregister.EBITDA=data['EBITDA']
    kpiregister.GMV=data['GMV']
    kpiregister.numberEmployees=data['numberEmployees']
    kpiregister.fundRaising=data['fundRaising']
    kpiregister.CAC=data['CAC']
    kpiregister.activeClients=data['activeClients']
    #print(kpiregister)
    db.session.commit()

    return jsonify({'message' : 'The kpi register has been updated!'})

#Delete kpi register
@app.route('/api/v1/kpi/<kpiId>', methods=['DELETE'])
@token_required
def delete_kpi_register(current_user, kpiId):
    
    Kpi_register = KpiRegister.query.filter_by(kpiId=kpiId).first()

    if not Kpi_register:
        return jsonify({'message' : 'No kpi record found!'})

    db.session.delete(Kpi_register)
    db.session.commit()

    return jsonify({'message' : 'The kpi record has been deleted!'})

if __name__ == "__main__":
    app.run(debug=True)
