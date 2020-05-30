from flask_restful import reqparse, Resource
from models.models import ResetCode, User
from exceptions.exceptions import UserUnauthorizedError, UserNotFoundError
from services.email_sender import email_sender_service
from services.authentication import auth_service
from app import db
import secrets

#/reset-codes
class ResetCodesRoutes(Resource):
    def __init__(self):
        super(ResetCodesRoutes, self).__init__()

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)        
        
        args = parser.parse_args()

        email = args['email']
        
        user = User.query.filter_by(email=email).first()
        
        if (not user):
            raise UserNotFoundError(f"No user found with email {email}.")
        
        code = secrets.token_urlsafe(4)
        reset_code = ResetCode(code=code,user=user)

        db.session.add(reset_code)
        db.session.commit()

        email_sender_service.send_reset_password_email(email, code)

        return {'message': 'ok'}, 200    

#/change-password-with-reset-code
class ChangePasswordRoutes(Resource):
    def __init__(self):
            super(ChangePasswordRoutes, self).__init__()

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)
        parser.add_argument("password", location="json", required=True, help="Missing user's password.", type=str)
        parser.add_argument("code", location="json", required=True, help="Missing user's reset code.", type=str)
        
        args = parser.parse_args()

        password = args['password']
        code = args['code']
        email = args['email']

        reset_code = ResetCode.query.filter_by(code=code).first()

        if (not reset_code):
            raise UserUnauthorizedError("Reset code does not exist.")
        

        if (reset_code.has_expired()):
            raise UserUnauthorizedError("Reset code has expired.")

        user = reset_code.user

        if(user.email != email):
            raise UserUnauthorizedError(f"Reset code does not belong to the email sent.")

        auth_service.update_password(email, password)

        db.session.delete(reset_code)
        db.session.commit()
        
        return {'message': 'ok'}, 200