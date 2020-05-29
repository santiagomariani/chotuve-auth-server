from flask_restful import reqparse, Resource
from utils.decorators import check_token, check_token_and_get_user
from app import db
from exceptions.exceptions import UserUnauthorizedError, UserNotFoundError
from models.models import User, user_schema


#/users
class UsersRoutes(Resource):
    def __init__(self):
        super(UsersRoutes, self).__init__()

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

        return {'message': 'ok'}, 200


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
        return user_schema.jsonify(user), 200
        
    @check_token_and_get_user
    def put(self, user, user_id):

        parser = reqparse.RequestParser()

        parser.add_argument("display_name", location="json", required=False, type=str)
        parser.add_argument("email", location="json", required=False, type=str)
        parser.add_argument("phone_number", location="json", required=False, type=str)
        parser.add_argument("image_location", location="json", required=False, type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token.")
        
        if not user.admin:
            if user.id != user_id:
                raise UserUnauthorizedError(f"User with ID: {user_id} cannot change other user's data. ")

        user_to_modify = User.query.filter_by(id=user_id).first()

        if not user_to_modify:
            raise UserNotFoundError(f"No user found with ID: {user_id}")

        if 'email' in args:
            user_to_modify.email = args['email']
        if 'display_name' in args:
            user_to_modify.display_name = args['display_name']
        if 'image_location' in args:
            user_to_modify.image_location = args['image_location']
        if 'phone_number' in args:
            user_to_modify.phone_number = args['phone_number']
        
        db.session.commit() 
        return {'message': 'ok'}, 200
