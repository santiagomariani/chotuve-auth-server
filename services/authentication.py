from exceptions.exceptions import UserUnauthorizedError
import firebase_admin
import os
from firebase_admin import auth

class AuthenticationFirebase():

    def __init__(self):
        self.firebase_app = firebase_admin.initialize_app()

    def verify_id_token(self, token):
        try:
            user_data = auth.verify_id_token(token)
        except auth.RevokedIdTokenError:
            raise UserUnauthorizedError(f"Token has been revoked.")
        except auth.ExpiredIdTokenError:
            raise UserUnauthorizedError(f"Token has expired.")
        except (auth.InvalidIdTokenError, ValueError):
            raise UserUnauthorizedError(f"Token is invalid.")
        return user_data

    def update_password(self, email, password):
        user_data = auth.get_user_by_email(email)
        uid = user_data.uid
        auth.update_user(uid, password=password)


class AuthenticationFake():

    def __init__(self):
        self.user_data = {'email': 'santiagomariani2@gmail.com', 'uid': '4cNAU9ovw6eD0KH5Qq7S91CXIZx2'}
        
        self.expiredToken = False
        self.revokedToken = False
        self.invalidToken = False

    def verify_id_token(self, token):
        if self.revokedToken:
            raise UserUnauthorizedError(f"Token has been revoked.")
        if self.expiredToken:
            raise UserUnauthorizedError(f"Token has expired.")
        if self.invalidToken:
            raise UserUnauthorizedError(f"Token is invalid.")
        return self.user_data
    
    def update_password(self, email, password):
        return True

    def setExpiredToken(self):
        self.expiredToken = True
        self.revokedToken = False
        self.invalidToken = False

    def setRevokedToken(self):
        self.revokedToken = True
        self.expiredToken = False
        self.invalidToken = False
    
    def setInvalidToken(self):
        self.invalidToken = True
        self.expiredToken = False
        self.revokedToken = False

    def setValidToken(self):
        self.invalidToken = False
        self.expiredToken = False
        self.revokedToken = False

auth_service = AuthenticationFirebase() if os.environ['APP_SETTINGS'] != 'testing' else AuthenticationFake()
