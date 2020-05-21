from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from models.user import User, user_schema
from app import db
from run import app
from firebase import auth
from functools import wraps
import pdb 
import time

def mock_verificar_token(token):
    time.sleep(0.2)
    #raise auth.ExpiredIdTokenError("hola","chau")
    #raise auth.RevokedIdTokenError("hola")
    #raise ValueError
    raise auth.InvalidIdTokenError("hola")
    return {'email': 'santiagofernandez@gmail.com', 'uid': '52151515215'}

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            mock_verificar_token(token)
            #auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'token has been revoked'}), 401
        except auth.ExpiredIdTokenError:
            return jsonify({'message': 'token has expired'}), 401
        except (auth.InvalidIdTokenError, ValueError):
            return jsonify({'message': 'token is invalid'}), 401
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
            mock_verificar_token(token)
            #auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            return jsonify({'message': 'token has been revoked'}), 401
        except auth.ExpiredIdTokenError:
            return jsonify({'message': 'token has expired'}), 401
        except (auth.InvalidIdTokenError, ValueError):
            return jsonify({'message': 'token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/sign-up', methods=['POST'])
@check_token
def sign_up():
    # create user in auth server database.
    data = request.json
    print(data)
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

@app.route('/users/<id>', methods=['GET'])
@check_token
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message' : 'user doesnt exist'}), 404
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
@check_token_and_get_user
def modify_user(user, id):
    print(type(user))
    print("ID")
    print(user.id)
    print(id)
    if not user.admin:
        if user.id != id:
            return jsonify({'message': 'normal user cannot change other users data'}), 401 
    data = request.json

    if 'email' in data:
        user.email = data['email']
    if 'display_name' in data:
        user.display_name = data['display_name']
    if 'image_location' in data:
        user.image_location = data['image_location']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']
    
    return user_schema.jsonify(user), 200

