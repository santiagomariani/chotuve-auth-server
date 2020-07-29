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
            return make_response({'message' : "Missing user's token."}, 400)

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
            return make_response({'message' : "Missing user's token."}, 400)

        user_data = auth_service.verify_id_token(token)
        user = User.query.filter_by(email=user_data['email']).first()
        return f(user, *args, **kwargs)
    return decorated

"""
def cross_origin(origin="*"):
    def cross_origin(func):
        @wraps(func)
        def _decoration(*args, **kwargs):
            ret = func(*args, **kwargs)
            _cross_origin_header = {"Access-Control-Allow-Origin": origin,
                                    "Access-Control-Allow-Headers":
                                        "Origin, X-Requested-With, Content-Type, Accept"}
            if isinstance(ret, tuple):
                if len(ret) == 2 and isinstance(ret[0], dict) and isinstance(ret[1], int):
                    # this is for handle response like: ```{'status': 1, "data":"ok"}, 200```
                    return ret[0], ret[1], _cross_origin_header
                elif isinstance(ret, basestring):
                    response = make_response(ret)
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return response
                elif isinstance(ret, Response):
                    ret.headers["Access-Control-Allow-Origin"] = origin
                    ret.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return ret
                else:
                    raise ValueError("Cannot handle cross origin, because the return value is not matched!")
            return ret

        return _decoration

    return cross_origin
"""