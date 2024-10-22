from flask_restful import reqparse, Resource
from models.models import ResetCode, User
from exceptions.exceptions import UserUnauthorizedError, UserNotFoundError
from services.email_sender import email_sender_service
from services.authentication import auth_service
from flask import make_response
from app import db
import logging

#/reset-codes
class ResetCodesRoutes(Resource):
    def __init__(self):
        super(ResetCodesRoutes, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("email", location="json", required=True, help="Missing user's email.", type=str)        
        
        args = parser.parse_args()

        email = args['email']
        
        user = User.query.filter_by(email=email).first()
        
        if (not user):
            self.logger.error(f"No user found with email: {email}. RESPONSECODE:404")
            raise UserNotFoundError(f"No user found.")
        
        reset_code = ResetCode(user)

        db.session.add(reset_code)
        db.session.commit()

        email_sender_service.send_reset_password_email(email, reset_code.code)

        self.logger.info(f"Reset code sent to email: {email}. RESPONSECODE:200")
        return make_response({'message': 'ok'}, 200)

#/change-password-with-reset-code
class ChangePasswordRoutes(Resource):
    def __init__(self):
        super(ChangePasswordRoutes, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

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
            self.logger.error(f"Reset code of user with email: {email} is not valid. RESPONSECODE:401")
            raise UserUnauthorizedError("Reset code is invalid.")

        if (reset_code.has_expired()):
            self.logger.error(f"Reset code of user with email: {email} has expired. RESPONSECODE:401")
            raise UserUnauthorizedError("Reset code has expired.")

        user = reset_code.user

        if(user.email != email):
            self.logger.error(f"Reset code of user with email: {email} is not valid. RESPONSECODE:401")
            raise UserUnauthorizedError(f"Reset code is invalid.")

        auth_service.update_password(email, password)

        db.session.delete(reset_code)
        db.session.commit()
        
        self.logger.info(f"Password of user with email: {email} has changed successfully. RESPONSECODE:200")

        return make_response({'message': 'ok'}, 200)