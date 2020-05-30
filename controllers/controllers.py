#import pdb 

#from flask import Flask, jsonify, request, session, redirect, url_for, make_response

from utils.decorators import check_token, check_token_and_get_user
from resources.users_routes import UsersRoutes, UniqueUserRoutes, UserIdFromTokenRoute
from resources.reset_codes import ResetCodesRoutes, ChangePasswordRoutes
from app import api
from run import app

api.add_resource(UsersRoutes, '/users')
api.add_resource(UniqueUserRoutes, '/users/<int:user_id>')
api.add_resource(UserIdFromTokenRoute, '/users/id')

api.add_resource(ResetCodesRoutes, '/reset-codes')
api.add_resource(ChangePasswordRoutes, '/change-password-with-reset-code')


@app.route('/ping')
def ping():
    return jsonify({'message': 'ok'}), 200

"""
@app.route('/users-test', methods=['POST'])
def create_user_delete_this():
    user = User(display_name="Sebastian Perez",
                email="sebastianperez@gmail.com",
                phone_number="2254450852",
                image_location="http://www.google.com.ar/imagen.jpeg")
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'ok'}), 200
"""
#-----------------------------------------------------

"""
def mock_verificar_token(token):
    time.sleep(0.2)
    #raise auth.ExpiredIdTokenError("hola","chau")
    #raise auth.RevokedIdTokenError("hola")
    #raise ValueError
    #raise auth.InvalidIdTokenError("hola")
    return {'email': 'santiagofernandez@gmail.com', 'uid': '52151515215'}

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing.'}), 401

        try:
            #mock_verificar_token(token)
            auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'token has been revoked.'}), 401
        except auth.ExpiredIdTokenError:
            return jsonify({'message': 'token has expired.'}), 401
        except (auth.InvalidIdTokenError, ValueError):
            return jsonify({'message': 'token is invalid.'}), 401
        return f(*args, **kwargs)
    return decorated

def check_token_and_get_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            #user_data = mock_verificar_token(token)
            user_data = auth.verify_id_token(token)
            user = User.query.filter_by(email=user_data['email']).first()
        except (auth.ExpiredIdTokenError, ValueError):
            return jsonify({'message': 'token is invalid'}), 401
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'token has been revoked'}), 401
        except auth.ExpiredIdTokenError:
            return jsonify({'message': 'token has expired'}), 401
        return f(user, *args, **kwargs)
    return decorated


@app.route('/users', methods=['POST'])
@check_token
def sign_up():
    # create user in auth server database.
    data = request.json
    user = User(email=data['email'],
        display_name=data['display_name'],
        phone_number=data['phone_number'],
        image_location=data['image_location'],
        admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'ok'}), 200
"""
@app.route('/sign-in', methods=['POST'])
@check_token
def sign_in():
    return jsonify({'message': 'ok'}), 200
"""
@app.route('/users/<id>', methods=['GET'])
@check_token
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message' : 'user doesnt exist.'}), 404
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
@check_token_and_get_user
def modify_user(user, id):
    if not user.admin:
        if user.id != id:
            return jsonify({'message': 'normal user cannot change other users data.'}), 401 
    data = request.json

    user_to_modify = User.query.filter_by(id=id).first()

    if not user_to_modify:
        return jsonify({'message' : 'user doesnt exist.'}), 404

    if 'email' in data:
        user_to_modify.email = data['email']
    if 'display_name' in data:
        user_to_modify.display_name = data['display_name']
    if 'image_location' in data:
        user_to_modify.image_location = data['image_location']
    if 'phone_number' in data:
        user_to_modify.phone_number = data['phone_number']
    
    db.session.commit() 
    return jsonify({'message': 'ok'}), 200

@app.route('/reset-codes', methods=['POST'])
def create_reset_code():
    data = request.json
    if ('email' not in data):
        return jsonify({'message': 'must send email.'}), 400

    email = data['email']
    user = User.query.filter_by(email=email).first()
    
    if (not user):
        return jsonify({'message': 'user does not exist.'}), 404
    
    code = secrets.token_urlsafe(4)
    reset_code = ResetCode(code=code,user=user)

    db.session.add(reset_code)
    db.session.commit()

    email_sender = EmailSender(email)
    email_sender.send_reset_password_email(code)
    return jsonify({'message': 'ok'}), 200

@app.route('/change-password-with-reset-code', methods=['POST'])
def validate_reset_code():
    data = request.json

    if ('password' not in data):
        return jsonify({'message': 'must send password.'}), 400

    if ('code' not in data):
        return jsonify({'message': 'must send reset code.'}), 400

    if ('email' not in data):
        return jsonify({'message': 'must send email.'}), 400

    password = data['password']
    code = data['code']
    email = data['email']

    reset_code = ResetCode.query.filter_by(code=code).first()

    if (not reset_code):
        return jsonify({'message': 'reset code does not exist.'}), 401

    user = reset_code.user

    if (reset_code.has_expired()):
        return jsonify({'message': 'reset code has expired.'}), 401

    if(user.email != email):
        return jsonify({'message': 'reset code does not belong to the email sent.'}), 401

    user_data = auth.get_user_by_email(user.email)
    uid = user_data.uid
    auth.update_user(uid, password=password)

    db.session.delete(reset_code)
    db.session.commit()
    
    return jsonify({'message': 'ok'}), 200
"""




    




