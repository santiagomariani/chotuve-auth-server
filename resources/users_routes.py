from flask_restful import reqparse, Resource
from flask import make_response
from utils.decorators import check_token, check_token_and_get_user
from app import db
from exceptions.exceptions import UserUnauthorizedError, UserNotFoundError
from models.models import User, user_schema, users_schema
import logging
from services.authentication import auth_service
from sqlalchemy import or_, sql

#/users
class UsersRoutes(Resource):
    def __init__(self):
        super(UsersRoutes, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    @check_token
    def get(self):
        parser = reqparse.RequestParser()

        # search
        parser.add_argument('email', type=str, required=False, location='args')
        parser.add_argument('phone', type=str, required=False, location='args')
        parser.add_argument('name', type=str, required=False, location='args')

        # pagination params
        parser.add_argument('per_page', type=int, required=False, location='args')
        parser.add_argument('page', type=int, required=False, location='args')

        args = parser.parse_args()

        query = User.query.filter(sql.false())

        if args['email']:
            query1 = User.query.filter(User.email.contains(args['email']))
            query = query.union(query1)

        if args['phone']:
            query2 = User.query.filter(User.phone_number.contains(args['phone']))
            query = query.union(query2)
            
        if args['name']:
            query3 = User.query.filter(User.display_name.contains(args['name']))
            query = query.union(query3)

        not_searching = not args['email'] and not args['phone'] and not args['name']

        if (not_searching):
            query = User.query

        # TODO: probablemente tenga que hacer que per_page y page sean obligatorios.
        # En la realidad no seria posible devolver todos los datos.
        if args['per_page'] and args['page']:
            pagination = query.paginate(per_page=args['per_page'], page=args['page'])
            items = pagination.items
            page_number = pagination.page
            return make_response({
                'users': users_schema.dump(items),
                'total': query.count(),
                'page': page_number
                }, 200)

        return make_response({'users': users_schema.dump(query.all())}, 200)

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("display_name", location="json", required=True, help="Missing user's display name.", type=str)
        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("phone_number", location="json", required=False, default="", type=str)
        parser.add_argument("image_location", location="json", required=False, default="", type=str)
        parser.add_argument("x-access-token", location='headers', required=True, help="Missing user's token.")

        args = parser.parse_args()

        email_associated_with_token = auth_service.verify_id_token(args['x-access-token'])['email']

        if email_associated_with_token != args['email']:
            raise UserUnauthorizedError(f"Token is invalid.")

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
                raise UserUnauthorizedError(f"Only admins can change others users data.")

        user_to_modify = User.query.filter_by(id=user_id).first()

        if not user_to_modify:
            raise UserNotFoundError(f"No user found with ID: {user_id}.")

        if args['email']:
            user_to_modify.email = args['email']
        if args['display_name']:
            user_to_modify.display_name = args['display_name']
        if args['image_location']:
            user_to_modify.image_location = args['image_location']
        if args['phone_number']:
            user_to_modify.phone_number = args['phone_number']
        
        db.session.commit()
        response = make_response(user_schema.jsonify(user_to_modify), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    def options(self, user_id):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
   

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