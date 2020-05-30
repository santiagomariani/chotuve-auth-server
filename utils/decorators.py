from services.authentication import auth_service
from models.models import User
from flask import Flask, jsonify, request, make_response
from functools import wraps

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message' : 'Missing user token!'}, 401)

        auth_service.verify_id_token(token)
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

        user_data = auth_service.verify_id_token(token)
        user = User.query.filter_by(email=user_data['email']).first()
        return f(user, *args, **kwargs)
    return decorated