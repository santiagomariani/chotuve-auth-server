from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from models.user import User, user_schema
from app import db
from run import app
from firebase import auth
from functools import wraps
import pdb 

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            auth.verify_id_token(token)
        except (auth.ExpiredIdTokenError, ValueError):
            return jsonify({'message': 'token is invalid'}), 401
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'token has been revoked'}), 401
        except auth.ExpiredIdTokenError:
            return jsonify({'message': 'token has expired'}), 401
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

@app.route('/sign-up', methods=['POST'])
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

@app.route('/sign-in', methods=['POST'])
@check_token
def sign_in():
    return jsonify({'message': 'ok'}), 200

"""

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            user_info = auth.get_account_info(token)
            pdb.set_trace()
            current_user = User.query.filter_by(email=user_info['email']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
"""

@app.route('/users/<id>', methods=['GET'])
@check_token
def get_user(id):
    user = User.query.filter_by(id=user_info['id']).first()
    if not user:
        return jsonify({'message' : 'user doesnt exist'}), 404
    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['PUT'])
@check_token_and_get_user
def modify_user(user, id):
    if not user.admin:
        if user.id != id:
            return jsonify({'message': 'normal user cannot change other users data'}), 401 
    data = request.json

    if not user:
        return jsonify({'message' : 'user doesnt exist'}), 404


