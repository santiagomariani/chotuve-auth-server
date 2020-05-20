from flask import Flask, jsonify, request, session, redirect, url_for, make_response
from models.user import User, user_schema
from app import db
from run import app
from firebase import auth
from functools import wraps
import pdb 

"""
@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json
    
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = data['phone_number']
    image_location = data['image_location']

    token = request.headers['x-access-token']
    auth.verify_id_token(token)

    #create user in firebase
    auth.create_user_with_email_and_password(email, password)

    #create user in my database
    user = User(email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        image_location=image_location)

    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

"""

@app.route('/sign-in', methods=['POST'])
def sign_in():
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
        return jsonify({'message': 'token has expired'})
    return jsonify({'message': 'ok'})

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

@app.route('/users/<id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    return user_schema.jsonify(current_user)
"""

@app.route('/', methods=['GET'])
def hello():
    return "hola flaco!"
