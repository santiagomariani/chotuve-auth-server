from firebase import auth
from models.models import User
from flask import Flask, jsonify, request, make_response
from functools import wraps
import time

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
            return make_response({'message' : 'Missing user token!'}, 401)

        try:
            #mock_verificar_token(token)
            auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            return make_response({'message' : 'Token has been revoked.'}, 401)
        except auth.ExpiredIdTokenError:
            return make_response({'message' : 'Token has expired.'}, 401) 
        except (auth.InvalidIdTokenError, ValueError):
            return make_response({'message': 'token is invalid.'}, 401)
        return f(*args, **kwargs)
    return decorated

def check_token_and_get_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message' : 'Missing user token!'}, 401)

        try:
            #user_data = mock_verificar_token(token)
            user_data = auth.verify_id_token(token)
            user = User.query.filter_by(email=user_data['email']).first()
        except auth.RevokedIdTokenError:
            return make_response({'message' : 'Token has been revoked.'}, 401)
        except auth.ExpiredIdTokenError:
            return make_response({'message' : 'Token has expired.'}, 401) 
        except (auth.InvalidIdTokenError, ValueError):
            return make_response({'message': 'token is invalid.'}, 401)
        return f(user, *args, **kwargs)
    return decorated