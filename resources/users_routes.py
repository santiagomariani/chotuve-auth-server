from flask_restful import reqparse, Resource
from flask import make_response
from utils.decorators import check_token, check_token_and_get_user
from app import db
from exceptions.exceptions import UserUnauthorizedError, UserNotFoundError
from models.models import User, user_schema, users_schema
import logging

#/users
class UsersRoutes(Resource):
    def __init__(self):
        super(UsersRoutes, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    @check_token
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', type=str, required=False, location='args')
        parser.add_argument('phone', type=str, required=False, location='args')
        parser.add_argument('name', type=str, required=False, location='args')

        args = parser.parse_args()

        query = User.query
        
        if args['email']:
            query = query.filter(User.email == args['email'])
        if args['phone']:
            print(args['phone'])
            query = query.filter(User.phone_number == args['phone'])
        if args['name']:
            query = query.filter(User.display_name.contains(args['name']))
        return make_response({'users': users_schema.dump(query.all())}, 200)

    @check_token
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("display_name", location="json", required=True, help="Missing user's display name.", type=str)
        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("phone_number", location="json", required=False, default="", type=str)
        parser.add_argument("image_location", location="json", required=False, default="", type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token.")

        args = parser.parse_args()

        user = User(email=args['email'],
                    display_name=args['display_name'],
                    phone_number=args['phone_number'],
                    image_location=args['image_location'],
                    admin=False)

        db.session.add(user)
        db.session.commit()

        return make_response(user_schema.jsonify(user), 201)


#/users/<int:user_id>
class UniqueUserRoutes(Resource):
    def __init__(self):
        super(UniqueUserRoutes, self).__init__()
    
    @check_token
    def get(self, user_id):

        parser = reqparse.RequestParser()

        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token")
        
        args = parser.parse_args()

        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            raise UserNotFoundError(f"No user found with ID: {user_id}")
        return make_response(user_schema.jsonify(user), 200)
        
    @check_token_and_get_user
    def put(user, self, user_id):

        parser = reqparse.RequestParser()

        parser.add_argument("display_name", location="json", required=False, type=str)
        parser.add_argument("email", location="json", required=False, type=str)
        parser.add_argument("phone_number", location="json", required=False, type=str)
        parser.add_argument("image_location", location="json", required=False, type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token.")
        
        args = parser.parse_args()
                
        if not user.admin:
            if user.id != user_id:
                raise UserUnauthorizedError(f"Only admins can change other users data.")

        user_to_modify = User.query.filter_by(id=user_id).first()

        if not user_to_modify:
            raise UserNotFoundError(f"No user found with ID: {user_id}")

        if args['email']:
            user_to_modify.email = args['email']
        if args['display_name']:
            user_to_modify.display_name = args['display_name']
        if args['image_location']:
            user_to_modify.image_location = args['image_location']
        if args['phone_number']:
            user_to_modify.phone_number = args['phone_number']
        
        db.session.commit() 
        return make_response(user_schema.jsonify(user_to_modify), 200)

#/users/id
class UserIdFromTokenRoute(Resource):
    def __init__(self):
        super(UserIdFromTokenRoute, self).__init__()

    @check_token_and_get_user
    def get(user, self):
        print(type(user))
        parser = reqparse.RequestParser()
        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token.")
        args = parser.parse_args()
        return make_response({'uid': user.id}, 200)